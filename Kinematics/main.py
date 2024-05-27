'''
Units:
 - cm
 - degrees

We need four angles:
 - Angle d = base angles
 - Angle a = shoulder angle
 - Angle b = elbow angle
 - Angle c = wrist angle(orinetation of end effector)

We need 4 lengths:
 - Height h - base length(link 1)
 - Length L - shoulder-elbow length(link 2)
 - Length M - elbow-wrist length(link 3)
 - Length Q - wrist-shoulder length(36cm)

a  = f + g
b = acos[((M^2)+(L^2)-(Q^2)) / (2*L*M)]
c = -b - a + 2*pi
d = math.atan2(x, y)
============
f = atan2(z, s)
z = 30cm
s = 20cm
g = acos[ ((L^2)+(Q^2)-(M^2)) / (2*L*Q)]

'''
import math


class Kinematics:
    """
    Parent class for kinematic calculations.
    """

    def __init__(self, lengths=[], angles=[]):
        self.links = 4
        self.lengths = lengths
        self.angles = angles

    def set_lengths(self, lengths):
        if isinstance(lengths, list) and len(lengths) == 4:
            self.lengths = lengths
        else:
            raise ValueError("Lengths should be a list containing 4 values.")

    def get_lengths(self):
        return self.lengths

    # def set_og_angles(self, angles:list):
    #     if isinstance(angles, list) and len(angles) == 4:
    #         self.angles = angles
    #     else:
    #         raise ValueError("Angles must be a list containing 4 values.")

    # def get_og_angles(self):
        # return self.angles

class ForwardKinematics(Kinematics):
    """
    Class for forward kinematic calculations.
    """

    def __init__(self):
      super().__init__()

    def calculate(self, link_lengths, initial_angles):
      lengths = link_lengths
      angles = initial_angles  # Convert angles to radians
      len_1, len_2, len_3, len_4 = lengths

      x_axis = len_1 * math.cos(angles[0]) + len_2 * math.cos(angles[0] + angles[1]) + \
                len_3 * math.cos(math.fsum(angles[:3])) + len_4 * math.cos(math.fsum(angles))
      y_axis = len_1 * math.sin(angles[0]) + len_2 * math.sin(angles[0] + angles[1]) + \
                len_3 * math.sin(math.fsum(angles[:3])) + len_4 * math.sin(math.fsum(angles))
      z_axis = 0.0  # Assuming 2D plane for simplicity

      orientation = math.fsum(angles[1:])  # Total of all joint angles except the first

      print(x_axis, y_axis, z_axis, orientation)
      return x_axis, y_axis, z_axis, orientation

class InverseKinematics(Kinematics):
    """
    Class for inverse kinematic calculations.
    """

    def __init__(self):
      # self.target_position = target_position
      self.z = 30
      self.s = 20
      super().__init__()


    # def set_target_position(self, target_position:list):
    #   if isinstance(target_position, list):
    #         self.target_position = target_position
    #   else:
    #       raise ValueError("target_position must be a list containing 3 values.")
      
    # def get_target_position(self):
    #     return self.target_position

    def calculate(self, link_lengths, target_position):
      '''
      We need four angles:
        - Angle d = base angles
        - Angle a = shoulder angle
        - Angle b = elbow angle
        - Angle c = wrist angle(orientation of end effector)
      '''
      a = self.calculate_angle_a(link_lengths)
      b = self.calculate_angle_b(link_lengths)
      c = self.calculate_angle_c(link_lengths)
      d = self.calculate_angle_d(target_position)
      rad_angles = (d, a, b, c)
      angles_in_degree = [math.degrees(angle) for angle in rad_angles]
      return angles_in_degree

    def calculate_angle_a(self, lengths):
      # lengths = self.get_lengths()
      f = math.atan2(self.z, self.s)
      L, Q, M = lengths[1], lengths[2], lengths[3]
      g = math.acos(((L**2) + (Q**2) - (M**2)) / (2*L*Q))
      angle_a = f + g
      return angle_a

    def calculate_angle_b(self, lengths):
      '''b = acos[((M^2)+(L^2)-(Q^2)) / (2*L*M)]'''
      # lengths = self.get_lengths()
      L, Q, M = lengths[1], lengths[2], lengths[3]
      angle_b = math.acos(((M**2) + (L**2) - (Q**2)) / (2*L*M))
      return angle_b

    def calculate_angle_c(self, lengths):
      '''c = -b - a + 2*pi'''
      b = self.calculate_angle_b(lengths)
      a = self.calculate_angle_a(lengths)
      pi = math.pi
      angle_c = -b - a + 2*pi
      return angle_c

    def calculate_angle_d(self, target_position):
      '''d = math.atan2(x, y)'''
      x, y = target_position[0], target_position[1]
      angle_d = math.atan2(y, x)
      return angle_d


if __name__ == "__main__":
#   # Define the link lengths
    link_lengths = [5, 10, 15, 8]  # [base, shoulder-elbow, elbow-wrist, wrist-end_effector]

#     # Define the initial joint angles (in degrees)
#     initial_angles = [0, 90, 0, 0]  # [base, shoulder, elbow, wrist]

#     kin = Kinematics()
#     # l_l = kin.set_lengths(link_lengths)
#     # l_l = kin.get_lengths()
    f_kin = ForwardKinematics()
    target_angles = [-155.58679708854172, 85.851292974163, 112.41113204623736, 161.73757497959963]
    angles_XYZ = f_kin.calculate(link_lengths, target_angles)
#     # l_l = f_kin.set_lengths(link_lengths)
#     # f_kin_l = f_kin.get_lengths()
#     # print(f"length of links: {f_kin_l}")

#     # Define the target position (x, y, z)
    # target_position = [0.0404651878368, 0.03711096706453477, 0.140101714]
    # i_ken = InverseKinematics()

    # angles_deg = i_ken.calculate(link_lengths, target_position)

#     # Convert angles from radians to degrees
    # angles_deg = [math.degrees(angle) for angle in angles]

    # print(f"Required joint angles (degrees) to reach target position {target_position}:")
    # print(f"Base angle (d): {angles_deg[0]:.2f}")
    # print(f"Shoulder angle (a): {angles_deg[1]:.2f}")
    # print(f"Elbow angle (b): {angles_deg[2]:.2f}")
    # print(f"Wrist angle (c): {angles_deg[3]:.2f}")