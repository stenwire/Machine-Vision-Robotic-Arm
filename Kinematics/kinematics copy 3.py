import numpy as np
from scipy.optimize import minimize

class Kinematics:
    def __init__(self, lengths=[], angles=[]):
        self._dof = 4
        self._links = 4
        self._link_lengths = lengths
        self._angles = angles

    def set_lengths_of_links(self, lengths):
        if isinstance(lengths, list) and len(lengths) == 4:
            self._link_lengths = lengths
        else:
            print("Lengths should be a list containing 4 values.")

    def get_lengths_of_links(self):
        return self._link_lengths
    
    def set_angles(self, angles):
        if isinstance(angles, list) and len(angles) == 4:
            self._angles = angles
        else:
            print("Angles must be a list containing 4 values.")

    def get_angles(self):
        return self._angles

class ForwardKinematics(Kinematics):
    def __init__(self):
        super().__init__()

    def calculate(self, angles=None):
        if angles is None:
            angles = self.get_angles()

        lengths = self.get_lengths_of_links()
        len_1, len_2, len_3, len_4 = lengths

        x_axis = len_1 * np.cos(np.radians(angles[0])) + len_2 * np.cos(np.radians(angles[0] + angles[1])) + \
                 len_3 * np.cos(np.radians(np.sum(angles[:3]))) + len_4 * np.cos(np.radians(np.sum(angles)))
        y_axis = len_1 * np.sin(np.radians(angles[0])) + len_2 * np.sin(np.radians(angles[0] + angles[1])) + \
                 len_3 * np.sin(np.radians(np.sum(angles[:3]))) + len_4 * np.sin(np.radians(np.sum(angles)))
        z_axis = 0.0  # Assuming 2D plane for simplicity

        orientation = np.sum(angles[1:])  # Orientation = Total of all joint angles except the first

        return x_axis, y_axis, z_axis, orientation

class InverseKinematics(Kinematics):
    def __init__(self):
        super().__init__()

    def ik_calculate(self, target_position):
        initial_angles = self.get_angles()
        result = minimize(self.objective_function, initial_angles, args=(target_position,), method='SLSQP')
        optimized_angles = result.x
        return optimized_angles

    def objective_function(self, angles, target_position):
        fk = ForwardKinematics()
        fk.set_lengths_of_links(self.get_lengths_of_links())
        x, y, _, _ = fk.calculate(angles)
        error = np.linalg.norm(np.array([x, y]) - target_position)
        return error

if __name__ == "__main__":
    lengths = [5, 10, 10, 7]
    f_kin = ForwardKinematics()
    f_kin.set_lengths_of_links(lengths)
    print("Lengths of links:", f_kin.get_lengths_of_links())

    f_kin.set_angles([20, 40, 60, 80])
    print("Forward kinematics result:", f_kin.calculate())

    # Example usage of inverse kinematics
    target_pos = np.array([-5.897090923213363, 15.316112512383063])  # Example target position from OpenCV
    ik = InverseKinematics()
    ik.set_lengths_of_links(lengths)
    ik.set_angles([0, 0, 0, 0]) # Position of the arm at that moment
    optimal_joint_angles = ik.ik_calculate(target_pos)
    print("Optimal joint angles from inverse kinematics:", optimal_joint_angles) # Position you want the arm to get to
