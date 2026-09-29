"""Shared data contracts. No image recognition algorithm is implemented here."""
from dataclasses import asdict, dataclass, field
import json
import math
from typing import Any, Literal
import numpy as np

COLORS = frozenset(('black', 'brown', 'red', 'orange', 'yellow', 'green',
                   'blue', 'violet', 'gray', 'white', 'gold', 'silver'))
REASONS = frozenset(('NO_OBJECT', 'MULTIPLE_OBJECTS', 'BLUR', 'UNDEREXPOSED',
                    'GLARE', 'BAND_COUNT', 'COLOR_AMBIGUOUS',
                    'DIRECTION_AMBIGUOUS', 'INVALID_CODE', 'UNSUPPORTED_CODE'))


def _image(image: np.ndarray) -> None:
    if (not isinstance(image, np.ndarray) or image.dtype != np.uint8
            or image.ndim != 3 or image.shape[2] != 3
            or min(image.shape[:2]) == 0):
        raise ValueError('Expected a nonempty uint8 HxWx3 BGR image')


def _mask(mask: np.ndarray, shape: tuple[int, int]) -> None:
    if (not isinstance(mask, np.ndarray) or mask.dtype != np.uint8
            or mask.shape != shape or not np.isin(mask, (0, 255)).all()):
        raise ValueError('Expected a matching uint8 mask with values 0 or 255')


@dataclass(frozen=True)
class FrameInput:
    image_bgr: np.ndarray
    frame_id: int
    timestamp_ms: float
    mode: Literal['card', 'resistor']

    def __post_init__(self):
        _image(self.image_bgr)
        if self.mode not in ('card', 'resistor'):
            raise ValueError('Unknown mode')
        if (not isinstance(self.frame_id, int) or isinstance(self.frame_id, bool)
                or self.frame_id < 0):
            raise ValueError('frame_id must be a nonnegative integer')
        if not math.isfinite(self.timestamp_ms) or self.timestamp_ms < 0:
            raise ValueError('Invalid timestamp')


@dataclass(frozen=True)
class QualityReport:
    passed: bool
    reasons: tuple[str, ...]
    blur_score: float
    dark_fraction: float
    glare_fraction: float

    def __post_init__(self):
        if not isinstance(self.passed, bool):
            raise ValueError('passed must be boolean')
        if not set(self.reasons).issubset(REASONS):
            raise ValueError('Unknown reason')
        if self.passed == bool(self.reasons):
            raise ValueError('Passed quality has no reasons; failed quality needs reasons')
        if not math.isfinite(self.blur_score) or self.blur_score < 0:
            raise ValueError('Invalid blur score')
        if not all(math.isfinite(v) and 0 <= v <= 1
                   for v in (self.dark_fraction, self.glare_fraction)):
            raise ValueError('Fractions must be finite and between 0 and 1')


@dataclass(frozen=True)
class NormalizedROI:
    image_bgr: np.ndarray
    valid_mask: np.ndarray
    body_mask: np.ndarray
    transform: np.ndarray
    inverse_transform: np.ndarray
    source_bbox: tuple[int, int, int, int]

    def __post_init__(self):
        _image(self.image_bgr)
        for mask in (self.valid_mask, self.body_mask):
            _mask(mask, self.image_bgr.shape[:2])
        if np.any((self.body_mask > 0) & (self.valid_mask == 0)):
            raise ValueError('Body must be inside the valid region')
        for matrix in (self.transform, self.inverse_transform):
            if (not isinstance(matrix, np.ndarray) or matrix.shape != (3, 3)
                    or not np.isfinite(matrix).all()):
                raise ValueError('Expected finite 3x3 matrices')
        if not np.allclose(self.transform @ self.inverse_transform, np.eye(3),
                           atol=1e-5):
            raise ValueError('Transforms are not inverses')
        x0, y0, x1, y1 = self.source_bbox
        if not (0 <= x0 < x1 and 0 <= y0 < y1):
            raise ValueError('source_bbox uses nonnegative half-open coordinates')


@dataclass(frozen=True)
class BandCandidate:
    candidate_id: str
    x0: int
    x1: int
    sample_mask: np.ndarray

    def __post_init__(self):
        if not self.candidate_id:
            raise ValueError('Candidate ID is required')
        if not isinstance(self.sample_mask, np.ndarray) or self.sample_mask.ndim != 2:
            raise ValueError('Sample mask must be two dimensional')
        _mask(self.sample_mask, self.sample_mask.shape)
        if not (isinstance(self.x0, int) and isinstance(self.x1, int)
                and 0 <= self.x0 < self.x1 <= self.sample_mask.shape[1]):
            raise ValueError('Band coordinates must be inside the ROI')
        if (not self.sample_mask.any() or self.sample_mask[:, :self.x0].any()
                or self.sample_mask[:, self.x1:].any()):
            raise ValueError('Sample pixels must be nonempty and inside the band')


@dataclass(frozen=True)
class ColorEvidence:
    candidate_id: str
    candidates: tuple[str, ...]
    rule_score: float
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.candidate_id or not set(self.candidates).issubset(COLORS):
            raise ValueError('Invalid candidate ID or color')
        if len(set(self.candidates)) != len(self.candidates):
            raise ValueError('Duplicate color candidates')
        if not math.isfinite(self.rule_score) or not 0 <= self.rule_score <= 1:
            raise ValueError('rule_score must be between 0 and 1; it is not a probability')


@dataclass(frozen=True)
class FrameResult:
    status: Literal['ACCEPT', 'REJECT']
    reason_codes: tuple[str, ...] = ()
    bands: tuple[str, ...] = ()
    direction: Literal['left_to_right', 'right_to_left'] | None = None
    resistance_ohm: float | None = None
    tolerance_percent: float | None = None
    diagnostics: dict[str, Any] = field(default_factory=dict)
    schema_version: str = field(default='1.0', init=False)

    def __post_init__(self):
        if not set(self.reason_codes).issubset(REASONS):
            raise ValueError('Unknown rejection reason')
        if not set(self.bands).issubset(COLORS):
            raise ValueError('Unknown color')
        if self.status == 'ACCEPT':
            if self.reason_codes or len(self.bands) != 4:
                raise ValueError('ACCEPT requires four bands and no rejection reasons')
            if self.direction not in ('left_to_right', 'right_to_left'):
                raise ValueError('ACCEPT requires a resolved direction')
            for value in (self.resistance_ohm, self.tolerance_percent):
                if value is None or not math.isfinite(value) or value <= 0:
                    raise ValueError('ACCEPT requires positive finite values')
            if self.tolerance_percent > 100:
                raise ValueError('Invalid tolerance percentage')
        elif self.status == 'REJECT':
            if not self.reason_codes:
                raise ValueError('REJECT requires a reason')
            if self.resistance_ohm is not None or self.tolerance_percent is not None:
                raise ValueError('REJECT must not carry a numerical reading')
        else:
            raise ValueError('Unknown result status')

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-compatible values. Diagnostics must already be JSON-safe."""
        return json.loads(json.dumps(asdict(self), allow_nan=False))


@dataclass(frozen=True)
class ScanResult:
    state: Literal['SEARCHING', 'ADJUST', 'READING', 'LOCKED']
    result: FrameResult | None
    track_id: str | None
    stable_duration_ms: float

    def __post_init__(self):
        if self.state not in ('SEARCHING', 'ADJUST', 'READING', 'LOCKED'):
            raise ValueError('Unknown scan state')
        if not math.isfinite(self.stable_duration_ms) or self.stable_duration_ms < 0:
            raise ValueError('Invalid duration')
        if self.state == 'LOCKED' and (not self.track_id or self.result is None
                                      or self.result.status != 'ACCEPT'):
            raise ValueError('LOCKED requires an accepted result and a track ID')
