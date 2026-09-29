"""Boundary checks for contracts; not image-recognition accuracy tests."""
import unittest
import numpy as np
from resfi.contracts import (FrameInput, QualityReport, NormalizedROI,
                             BandCandidate, ColorEvidence, FrameResult, ScanResult)


class ContractsTest(unittest.TestCase):
    def setUp(self):
        self.image = np.zeros((10, 20, 3), dtype=np.uint8)
        self.mask = np.full((10, 20), 255, dtype=np.uint8)

    def accepted(self, **overrides):
        fields = dict(status='ACCEPT', bands=('yellow', 'violet', 'red', 'gold'),
                      direction='left_to_right', resistance_ohm=4700., tolerance_percent=5.)
        fields.update(overrides)
        return FrameResult(**fields)

    def test_valid_frame(self):
        self.assertEqual(FrameInput(self.image, 0, 0., 'card').mode, 'card')

    def test_invalid_images_rejected(self):
        for image in (np.zeros((10, 20), dtype=np.uint8), self.image.astype(float),
                      np.zeros((0, 20, 3), dtype=np.uint8)):
            with self.subTest(shape=image.shape), self.assertRaises(ValueError):
                FrameInput(image, 0, 0., 'card')

    def test_bad_mode_and_time(self):
        for mode, stamp in [('bad', 0), ('card', float('nan')), ('card', -1)]:
            with self.subTest(mode=mode, stamp=stamp), self.assertRaises(ValueError):
                FrameInput(self.image, 0, stamp, mode)

    def test_quality_requires_failure_reason(self):
        with self.assertRaises(ValueError):
            QualityReport(False, (), 2., 0., 0.)
        self.assertFalse(QualityReport(False, ('BLUR',), 2., 0., 0.).passed)

    def test_roi_transform_and_masks(self):
        roi = NormalizedROI(self.image, self.mask, self.mask, np.eye(3), np.eye(3), (0, 0, 20, 10))
        self.assertEqual(roi.image_bgr.shape, (10, 20, 3))
        with self.assertRaises(ValueError):
            NormalizedROI(self.image, self.mask, self.mask, np.eye(3)*2, np.eye(3), (0, 0, 20, 10))

    def test_body_cannot_include_padding(self):
        valid = self.mask.copy(); valid[:, 0] = 0
        with self.assertRaises(ValueError):
            NormalizedROI(self.image, valid, self.mask, np.eye(3), np.eye(3), (0, 0, 20, 10))

    def test_band_interval_and_sample_pixels(self):
        sample = np.zeros((10, 20), dtype=np.uint8); sample[:, 3:6] = 255
        self.assertEqual(BandCandidate('b1', 3, 6, sample).x1, 6)
        with self.assertRaises(ValueError):
            BandCandidate('b1', 4, 6, sample)

    def test_color_ambiguity_is_preserved(self):
        evidence = ColorEvidence('b1', ('brown', 'red'), .4)
        self.assertEqual(len(evidence.candidates), 2)
        with self.assertRaises(ValueError):
            ColorEvidence('b1', ('sari',), .4)

    def test_accept_serializes_lists_and_values(self):
        output = self.accepted().to_dict()
        self.assertEqual(output['bands'], ['yellow', 'violet', 'red', 'gold'])
        self.assertEqual(output['resistance_ohm'], 4700.)

    def test_reject_does_not_publish_stale_value(self):
        result = FrameResult('REJECT', ('NO_OBJECT',))
        self.assertIsNone(result.to_dict()['resistance_ohm'])
        with self.assertRaises(ValueError):
            FrameResult('REJECT', ('NO_OBJECT',), resistance_ohm=4700.)

    def test_accept_needs_direction_and_finite_value(self):
        for overrides in [dict(direction=None), dict(resistance_ohm=float('nan')),
                          dict(bands=('red',)), dict(status='UNKNOWN')]:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.accepted(**overrides)

    def test_json_nan_diagnostic_is_rejected(self):
        with self.assertRaises(ValueError):
            self.accepted(diagnostics={'score': float('nan')}).to_dict()

    def test_lock_needs_track_and_accept(self):
        with self.assertRaises(ValueError):
            ScanResult('LOCKED', FrameResult('REJECT', ('BLUR',)), 't1', 300.)
        self.assertEqual(ScanResult('LOCKED', self.accepted(), 't1', 300.).state, 'LOCKED')


if __name__ == '__main__':
    unittest.main()
