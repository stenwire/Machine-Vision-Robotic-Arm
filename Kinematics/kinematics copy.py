import numpy as np
from scipy.optimize import minimize

class Kinematics:
    """
    Parent class for kinematic calculations.
    """

    def __init__(self, lengths=[], angles=[]):
        self.links = 4
        self.set_lengths_of_links(lengths)
        self.set_angles(angles)

    def set_lengths_of_links(self, lengths):
        if isinstance(lengths, list) and len(lengths) == 4:
            self.link_lengths = lengths
        else:
            raise ValueError("Lengths should be a list containing 4 values.")

    def get_lengths_of_links(self):
        return self.link_lengths
    
    def set_angles(self, angles:list):
        if isinstance(angles, list) and len(angles) == 4:
            self.angles = angles
        else:
            raise ValueError("Angles must be a list containing 4 values.")

    def get_angles(self):
        return self.angles

class ForwardKinematics(Kinematics):
    """
    Class for forward kinematic calculations.
    """

    def calculate(self):
        lengths = self.get_lengths_of_links()
        angles = np.radians(self.get_angles())  # Convert angles to radians
        len_1, len_2, len_3, len_4 = lengths

        x_axis = len_1 * np.cos(angles[0]) + len_2 * np.cos(angles[0] + angles[1]) + \
                 len_3 * np.cos(np.sum(angles[:3])) + len_4 * np.cos(np.sum(angles))
        y_axis = len_1 * np.sin(angles[0]) + len_2 * np.sin(angles[0] + angles[1]) + \
                 len_3 * np.sin(np.sum(angles[:3])) + len_4 * np.sin(np.sum(angles))
        z_axis = 0.0  # Assuming 2D plane for simplicity

        orientation = np.sum(angles[1:])  # Total of all joint angles except the first

        return x_axis, y_axis, z_axis, orientation

class InverseKinematics(Kinematics):
    """
    Class for inverse kinematic calculations.
    """

    def calculate(self, og_angles, target_position):
        # print("Length of og_angles:", len(og_angles))
        initial_angles = np.radians(og_angles)  # Convert initial angles to radians
        # print("Length of initial_angles:", len(initial_angles))
        link_lengths = self.get_lengths_of_links()
        result = minimize(self.objective_function, initial_angles, args=(og_angles, target_position,), method='SLSQP')
        optimized_angles = np.degrees(result.x)  # Convert optimized angles to degrees before returning
        return optimized_angles

    def objective_function(self, angles, lengths, target_position):
        fk = ForwardKinematics(lengths=lengths, angles=np.degrees(angles))  # Convert angles to degrees for FK calculation
        x, y, _, _ = fk.calculate()
        error = np.linalg.norm(np.array([x, y]) - target_position)
        return error

if __name__ == "__main__":
    lengths = [1, 1, 1, 1]
    og_angles = [45, 30, 60, 90]

    # Example usage of forward kinematics
    f_kin = ForwardKinematics(lengths=lengths, angles=og_angles)
    print("Forward Kinematics, X and Y value:", f_kin.calculate()[:2])
    print("Length of og_angles:", len(f_kin.get_angles()))

    # Example usage of inverse kinematics
    target_pos = np.array([2.0, 2.0])  # Example target position from OpenCV
    ik = InverseKinematics(lengths=lengths, angles=og_angles)
    print("Length of og_angles:", len(ik.get_angles()))
    print("Length of og_angles:", len(og_angles))
    optimal_joint_angles = ik.calculate(og_angles, target_pos)
    # print("Optimal joint angles from inverse kinematics:", optimal_joint_angles)
