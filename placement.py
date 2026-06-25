import numpy as np

from config import PLACEMENT_MARGIN_MM, PLACEMENT_SPACING_MM


class PlacementPlanner:
    def __init__(self, margin_mm=PLACEMENT_MARGIN_MM, spacing_mm=PLACEMENT_SPACING_MM):
        self.margin_mm = margin_mm
        self.spacing_mm = spacing_mm
        self.workspace_world_points = []
        self.division_line_world_points = []
        self.candidates = []
        self.next_index = 0

    def reset(self):
        self.workspace_world_points = []
        self.division_line_world_points = []
        self.candidates = []
        self.next_index = 0

    def configure(
        self,
        workspace_world_points,
        division_line_world_points,
        is_inside_workspace_func,
        is_in_placement_zone_func,
    ):
        self.workspace_world_points = list(workspace_world_points)
        self.division_line_world_points = list(division_line_world_points)
        self.candidates = self._build_candidates(
            is_inside_workspace_func,
            is_in_placement_zone_func,
        )
        self.next_index = 0

    def next_place_point(self):
        if self.next_index >= len(self.candidates):
            raise RuntimeError("No free placement point is available inside the placement zone.")

        point = self.candidates[self.next_index]
        self.next_index += 1
        return point

    def _build_candidates(self, is_inside_workspace_func, is_in_placement_zone_func):
        if len(self.workspace_world_points) < 7:
            return []

        top_left = np.array(self.workspace_world_points[0], dtype=np.float32)
        top_right = np.array(self.workspace_world_points[2], dtype=np.float32)
        bottom_left = np.array(self.workspace_world_points[6], dtype=np.float32)

        top_vector = top_right - top_left
        down_vector = bottom_left - top_left
        top_length = float(np.linalg.norm(top_vector))
        down_length = float(np.linalg.norm(down_vector))

        if top_length == 0 or down_length == 0:
            return []

        top_unit = top_vector / top_length
        down_unit = down_vector / down_length
        candidates = []

        row_distance = self.margin_mm
        while row_distance <= down_length - self.margin_mm:
            col_distance = self.margin_mm
            while col_distance <= top_length - self.margin_mm:
                point = top_left + top_unit * col_distance + down_unit * row_distance
                xw = float(point[0])
                yw = float(point[1])

                if is_inside_workspace_func(xw, yw) and is_in_placement_zone_func(xw, yw):
                    candidates.append((xw, yw, 0))

                col_distance += self.spacing_mm
            row_distance += self.spacing_mm

        return candidates
