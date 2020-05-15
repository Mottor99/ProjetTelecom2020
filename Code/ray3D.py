import cmath
import math
from math import cos, sin
from transmitter3D import Transmitter
import numpy as np

class Ray:

    omega = 2 * math.pi * Transmitter.frequency
    epsilon0 = 8.854*10**-12
    mu0 = 4*math.pi*10**-7
    beta_air = omega * math.sqrt(mu0 * epsilon0)

    def __init__(self, list_of_points):
        self.list_of_points = list_of_points
        self.distance = 0
        self.polarisation = (0,0,-1)
        self.theta_emission = 0
        self.phi_emission = 0
        self.theta_reception = 0
        self.phi_reception = 0


    def reflection_perpendicular_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        #print("theta_i"+str(theta_i))
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_0 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_m = wall.intrinsic_impedance
        gamma_perp = (Z_m * cos(theta_i) - Z_0 * cos(theta_t)) / (Z_m * cos(theta_i) + Z_0 * cos(theta_t))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        gamma_wall = gamma_perp + (1 - gamma_perp ** 2) * (
                    gamma_perp * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
                1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t))) \
                     / (1 - (gamma_perp ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))

        #print("gamma wall normal")
        #print(gamma_wall)
        #print("gamma_wall:" + str(abs(gamma_wall)))

        return gamma_wall


    def transmission_perpendicular_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_0 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_m = wall.intrinsic_impedance
        gamma_perp = (Z_m * cos(theta_i) - Z_0 * cos(theta_t)) / (Z_m * cos(theta_i) + Z_0 * cos(theta_t))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        tau_wall = (1 - gamma_perp ** 2) * cmath.exp(-little_gamma_wall * s) \
                   / (1 - (gamma_perp ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))

        #print("tau wall normal")
        #print(tau_wall)
        #print("point1:"+str(wall.point2))
        #print("tau_wall:" + str(abs(tau_wall)))

        return tau_wall

    def reflection_parallel_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        #print("theta_i:" + str(theta_i))
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_0 = math.sqrt(self.mu0/epsilon_tilde_1)
        Z_m = wall.intrinsic_impedance
        gamma_parallel = (Z_m*cos(theta_t)-Z_0*cos(theta_i))/(Z_m*cos(theta_t)+Z_0*cos(theta_i))
        s = wall.thickness/cos(theta_t)
        little_gamma_wall = wall.little_gamma
        gamma_wall = gamma_parallel + (1 - gamma_parallel ** 2) * (
                gamma_parallel * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t))) \
                     / (1 - (gamma_parallel ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))
        """
        print("gamma_wall parallel")
        print(gamma_wall)
        """
        #print("gamma_wall:" + str(abs(gamma_wall)))
        return gamma_wall


    def transmission_parallel_coefficient_calculation(self, wall, ray_line):
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        #print("theta_i:" + str(theta_i))
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_0 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_m = wall.intrinsic_impedance
        gamma_parallel = (Z_m*cos(theta_t)-Z_0*cos(theta_i))/(Z_m*cos(theta_t)+Z_0*cos(theta_i))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        tau_wall = (1 - gamma_parallel ** 2) * cmath.exp(-little_gamma_wall * s) \
                   / (1 - (gamma_parallel ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))
        """
        print("tau wall parallel")
        print(tau_wall)
        """
        #print("tau_wall:" + str(abs(tau_wall)))
        return tau_wall

    def transmission_total_coefficient_calculation(self, wall, ray_line):
        a = np.dot(ray_line.direction_vector, wall.plane.normal_vector)
        b = ray_line.direction_vector - np.dot(2 * a, wall.plane.normal_vector)
        c = np.cross(ray_line.direction_vector, b)
        norm_c = np.linalg.norm(c)
        if norm_c == 0:
            c = ray_line.direction_vector
            norm_c = 1
        c = np.dot(1 / norm_c, c)

        tau_wall_perp = self.transmission_perpendicular_coefficient_calculation(wall, ray_line)
        tau_wall_para = self.transmission_parallel_coefficient_calculation(wall, ray_line)

        d = np.dot(c, self.polarisation)
        pola_perp = d * c
        pola_parallel = self.polarisation - np.dot(1, pola_perp)
        self.polarisation = np.dot(tau_wall_perp, pola_perp) + np.dot(tau_wall_para, pola_parallel)

        return 0




    def reflection_total_coefficient_calculation(self, wall, ray_line):
        a = np.dot(ray_line.direction_vector, wall.plane.normal_vector)
        b = ray_line.direction_vector - np.dot(2 * a, wall.plane.normal_vector)
        c = np.cross(ray_line.direction_vector, b)
        norm_c = np.linalg.norm(c)
        if norm_c == 0:
            c = (0, 0, -1)
            norm_c = 1
        c = np.dot(1 / norm_c, c)

        gamma_wall_perp = self.reflection_perpendicular_coefficient_calculation(wall, ray_line)
        gamma_wall_para = self.reflection_parallel_coefficient_calculation(wall, ray_line)


        d = np.dot(c,self.polarisation)
        #print(abs(d/np.linalg.norm(self.polarisation)))
        pola_perp = d*c
        pola_parallel = self.polarisation-np.dot(1, pola_perp)
        self.polarisation = np.dot(gamma_wall_perp, pola_perp) + np.dot(gamma_wall_para,pola_parallel)

        return 0
