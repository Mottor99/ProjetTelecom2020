import cmath
import math
from math import cos, sin

class Ray:

    omega = 2*math.pi*5*10**9
    epsilon0 = 8.854*10**-12
    mu0 = 4*math.pi*10**-7

    def __init__(self, list_of_points):
        self.list_of_points = list_of_points
        self.distance = 0
        self.angle_with_transmitter = 0
        self.reflection_coefficient = []
        self.transmission_coefficient = []

    def reflection_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.line.incident_angle_calculation(ray_line)
        theta_t = wall.line.transmitted_angle_calculation(wall, theta_i)
        print("calcul de theta")
        epsilon_tilde_1 = self.epsilon0
        """re_epsilon_tilde_2 = wall.permittivite
        im_epsilon_tilde_2 = -wall.conductivite/self.omega
        epsilon_tilde_2 = complex(re_epsilon_tilde_2, im_epsilon_tilde_2)"""
        Z_1 = math.sqrt(self.mu0/epsilon_tilde_1)
        Z_2 = wall.intrinsic_impedance
        gamma_perp = (Z_2*cos(theta_i)-Z_1*cos(theta_t))/(Z_2*cos(theta_i)+Z_1*cos(theta_t))
        s = wall.thickness/cos(theta_t)
        beta_air = self.omega*math.sqrt(self.mu0*self.epsilon0)
        little_gamma_wall = wall.little_gamma
        gamma_wall = gamma_perp + (1-gamma_perp**2)*(gamma_perp*cmath.exp(-2*little_gamma_wall*s)*cmath.exp(1j*beta_air*2*s*sin(theta_i)*sin(theta_t)))\
                     /(1-(gamma_perp**2)*cmath.exp(-2*little_gamma_wall*s)*cmath.exp(1j*beta_air*2*s*sin(theta_i)*sin(theta_t)))
        return gamma_wall

    def transmission_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.line.incident_angle_calculation(ray_line)
        theta_t = wall.line.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        """re_epsilon_tilde_2 = wall.permittivite
        im_epsilon_tilde_2 = -wall.conductivite / self.omega
        epsilon_tilde_2 = complex(re_epsilon_tilde_2, im_epsilon_tilde_2)"""
        Z_1 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_2 = wall.intrinsic_impedance
        gamma_perp = (Z_2 * cos(theta_i) - Z_1 * cos(theta_t)) / (Z_2 * cos(theta_i) + Z_1 * cos(theta_t))
        s = wall.thickness / cos(theta_t)
        beta_air = self.omega * math.sqrt(self.mu0 * self.epsilon0)
        little_gamma_wall = wall.little_gamma
        tau_wall = (1-gamma_perp**2)*cmath.exp(-little_gamma_wall*s)\
                   /(1-(gamma_perp**2)*cmath.exp(-2*little_gamma_wall*s)*cmath.exp(1j*beta_air*2*s*sin(theta_i)*sin(theta_t)))

        return tau_wall