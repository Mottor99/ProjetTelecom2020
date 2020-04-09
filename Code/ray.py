import cmath
import math
from math import cos, sin

class Ray:

    omega = 2*math.pi*5*10**9
    epsilon0 = 8.854*10**-12
    mu0 = 4*math.pi*10**-7

    def __init__(self, liste_de_points):
        self.liste_de_points = liste_de_points
        self.distance = 0
        self.angle_emetteur = 0
        self.coefficient_de_reflexion = []
        self.coefficient_de_transmission = []

    def reflection_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.line.incident_angle_calculation(ray_line)
        theta_t = wall.line.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = cmath.complex(self.epsilon0, 0)
        re_epsilon_tilde_2 = wall.permittivite
        im_epsilon_tilde_2 = -wall.conductivite/self.omega
        epsilon_tilde_2 = cmath.complex(re_epsilon_tilde_2, im_epsilon_tilde_2)
        Z_1 = math.sqrt(self.mu0/epsilon_tilde_1)
        Z_2 = math.sqrt(self.mu0/epsilon_tilde_2)
        gamma_perp = (Z_2*cos(theta_i)-Z_1*cos(theta_t))/(Z_2*cos(theta_i)+Z_1*cos(theta_t))
        s = wall.epaisseur/cos(theta_t)
        beta_air = self.omega*math.sqrt(self.mu0*self.epsilon0)
        beta_wall = wall.beta
        gamma_wall = gamma_perp + (1-gamma_perp**2)*(gamma_perp*cmath.exp(-2*1j*beta_wall*s)*cmath.exp(1j*beta_air*2*s*sin(theta_i)*sin(theta_t)))\
                     /(1-(gamma_perp**2)*cmath.exp(-2*1j*beta_wall*s)*cmath.exp(1j*beta_air*2*s*sin(theta_i)*sin(theta_t)))
        return gamma_wall

    def transmission_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.line.incident_angle_calculation(ray_line)
        theta_t = wall.line.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = cmath.complex(self.epsilon0, 0)
        re_epsilon_tilde_2 = wall.permittivite
        im_epsilon_tilde_2 = -wall.conductivite / self.omega
        epsilon_tilde_2 = cmath.complex(re_epsilon_tilde_2, im_epsilon_tilde_2)
        Z_1 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_2 = math.sqrt(self.mu0 / epsilon_tilde_2)
        gamma_perp = (Z_2 * cos(theta_i) - Z_1 * cos(theta_t)) / (Z_2 * cos(theta_i) + Z_1 * cos(theta_t))
        s = wall.epaisseur / cos(theta_t)
        beta_air = self.omega * math.sqrt(self.mu0 * self.epsilon0)
        beta_wall = wall.beta
        tau_wall = (1-gamma_perp**2)*cmath.exp(-1j*beta_wall*s)\
                   /(1-(gamma_perp**2)*cmath.exp(-2*1j*beta_wall*s)*cmath.exp(1j*beta_air*2*s*sin(theta_i)*sin(theta_t)))

        return tau_wall