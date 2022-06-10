from typing import List


class Gene:
    def __init__(self, code: List[float]) -> None:
        assert len(code) == Gene.length()
        self.code = code

    @staticmethod
    def length() -> int:
        return 17

    def __len__(self) -> int:
        return len(self.code)

    @property
    def link_shape(self) -> float:
        return self.code[0]

    @property
    def link_length(self) -> float:
        return self.code[1]

    @property
    def link_radius(self) -> float:
        return self.code[2]

    @property
    def link_recurrence(self) -> float:
        return self.code[3]

    @property
    def link_mass(self) -> float:
        return self.code[4]

    @property
    def joint_parent(self) -> float:
        return self.code[5]

    @property
    def joint_type(self) -> float:
        return self.code[6]

    @property
    def joint_axis_xyz(self) -> float:
        return self.code[7]

    @property
    def joint_origin_rpy_r(self) -> float:
        return self.code[8]

    @property
    def joint_origin_rpy_p(self) -> float:
        return self.code[9]

    @property
    def joint_origin_rpy_y(self) -> float:
        return self.code[10]

    @property
    def joint_origin_xyz_x(self) -> float:
        return self.code[11]

    @property
    def joint_origin_xyz_y(self) -> float:
        return self.code[12]

    @property
    def joint_origin_xyz_z(self) -> float:
        return self.code[13]

    @property
    def control_waveform(self) -> float:
        return self.code[14]

    @property
    def control_amp(self) -> float:
        return self.code[15]

    @property
    def control_freq(self) -> float:
        return self.code[16]
