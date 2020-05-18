import cmath
import math
from math import cos, sin
from transmitter3D import Transmitter
import numpy as np


class Ray:

    omega = 2 * math.pi * Transmitter.frequency
    epsilon0 = 8.854*10**-12
    mu0 = 4*math.pi*10**-7
    beta_air = 2*math.pi/Transmitter.wavelength

    def __init__(self, list_of_points):
        self.list_of_points = list_of_points
        self.distance = 0
        self.polarisation = (0,0,-1)
        self.theta_emission = 0
        self.phi_emission = 0
        self.theta_reception = 0
        self.phi_reception = 0

    def reflection_perpendicular_coefficient_calculation(self, wall, ray_line):
        """
        :param wall: mur où s'effectue la réflexion
        :param ray_line: segment de droit incident du rayon
        :return: coefficient de réflexion du mur pour une polarisation perpendiculaire
        """
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_1 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_2 = wall.intrinsic_impedance
        gamma_perp = (Z_2 * cos(theta_i) - Z_1 * cos(theta_t)) / (Z_2 * cos(theta_i) + Z_1 * cos(theta_t))
        if wall.epsilon_rel == 9:
            return gamma_perp
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        gamma_wall = gamma_perp + (1 - gamma_perp ** 2) * (
                    gamma_perp * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
                1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t))) \
                     / (1 - (gamma_perp ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))

        return gamma_wall


    def transmission_perpendicular_coefficient_calculation(self, wall, ray_line):
        """
        :param wall: mur où s'effectue la réflexion
        :param ray_line: segment de droit incident du rayon
        :return: coefficient de transmission du mur pour une polarisation perpendiculaire
        """
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_1 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_2 = wall.intrinsic_impedance
        gamma_perp = (Z_2 * cos(theta_i) - Z_1 * cos(theta_t)) / (Z_2 * cos(theta_i) + Z_1 * cos(theta_t))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        tau_wall = (1 - gamma_perp ** 2) * cmath.exp(-little_gamma_wall * s) \
                   / (1 - (gamma_perp ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))

        return tau_wall

    def reflection_parallel_coefficient_calculation(self, wall, ray_line):
        """
        :param wall: mur où s'effectue la réflexion
        :param ray_line: segment de droit incident du rayon
        :return: coefficient de réflexion du mur pour une polarisation parallèle
        """
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_1 = math.sqrt(self.mu0/epsilon_tilde_1)
        Z_2 = wall.intrinsic_impedance
        gamma_parallel = (Z_2*cos(theta_t)-Z_1*cos(theta_i))/(Z_2*cos(theta_t)+Z_1*cos(theta_i))
        if wall.epsilon_rel == 9:
            return gamma_parallel
        s = wall.thickness/cos(theta_t)
        little_gamma_wall = wall.little_gamma
        gamma_wall = gamma_parallel + (1 - gamma_parallel ** 2) * (
                gamma_parallel * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t))) \
                     / (1 - (gamma_parallel ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))
        return gamma_wall


    def transmission_parallel_coefficient_calculation(self, wall, ray_line):
        """
        :param wall: mur où s'effectue la réflexion
        :param ray_line: segment de droit incident du rayon
        :return: coefficient de transmission du mur pour une polarisation parallèle
        """
        theta_i = wall.plane.incident_angle_calculation(ray_line)
        theta_t = wall.plane.transmitted_angle_calculation(wall, theta_i)
        epsilon_tilde_1 = self.epsilon0
        Z_1 = math.sqrt(self.mu0 / epsilon_tilde_1)
        Z_2 = wall.intrinsic_impedance
        gamma_parallel = (Z_2*cos(theta_t)-Z_1*cos(theta_i))/(Z_2*cos(theta_t)+Z_1*cos(theta_i))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        tau_wall = (1 - gamma_parallel ** 2) * cmath.exp(-little_gamma_wall * s) \
                   / (1 - (gamma_parallel ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
            1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))
        return tau_wall

    def transmission_total_coefficient_calculation(self, wall, ray_line):
        """
        Modifie la polarisation totale du rayon après transmission
        :param wall: mur où s'effectue la réflexion
        :param ray_line: segment de droit incident du rayon
        """
        #calcul du vecteur perpendiculaire au plan d'incidence
        a = np.dot(ray_line.direction_vector, wall.plane.normal_vector)
        b = ray_line.direction_vector - np.dot(2 * a, wall.plane.normal_vector)
        c = np.cross(ray_line.direction_vector, b)
        norm_c = np.linalg.norm(c)
        if norm_c == 0:
            #cas limite
            c = ray_line.direction_vector
            norm_c = 1
        c = np.dot(1 / norm_c, c) #vecteur perpendiculaire au plan d'incidence

        #calcul des coefficients parallèles et perpendiculaire
        tau_wall_perp = self.transmission_perpendicular_coefficient_calculation(wall, ray_line)
        tau_wall_para = self.transmission_parallel_coefficient_calculation(wall, ray_line)

        # décomposition de la polarisation en une partie perpendiculaire
        # au plan d'incidence et une partie parallèle
        d = np.dot(c, self.polarisation)
        pola_perp = d * c
        pola_parallel = self.polarisation - np.dot(1, pola_perp)
        self.polarisation = np.dot(tau_wall_perp, pola_perp) + np.dot(tau_wall_para, pola_parallel)

        return 0




    def reflection_total_coefficient_calculation(self, wall, ray_line):
        """
        Modifie la polarisation totale du rayon après réflexion
        :param wall: mur où s'effectue la réflexion
        :param ray_line: segment de droit incident du rayon
        """
        # calcul du vecteur perpendiculaire au plan d'incidence
        a = np.dot(ray_line.direction_vector, wall.plane.normal_vector)
        b = ray_line.direction_vector - np.dot(2 * a, wall.plane.normal_vector)
        c = np.cross(ray_line.direction_vector, b)
        norm_c = np.linalg.norm(c)
        if norm_c == 0:
            # cas limite
            c = (0, 0, -1)
            norm_c = 1
        c = np.dot(1 / norm_c, c) #vecteur perpendiculaire au plan d'incidence

        #calcul des coefficients parallèles et perpendiculaire
        gamma_wall_perp = self.reflection_perpendicular_coefficient_calculation(wall, ray_line)
        gamma_wall_para = self.reflection_parallel_coefficient_calculation(wall, ray_line)

        # décomposition de la polarisation en une partie perpendiculaire
        # au plan d'incidence et une partie parallèle
        d = np.dot(c,self.polarisation)
        pola_perp = d*c
        pola_parallel = self.polarisation-np.dot(1, pola_perp)
        #calcul de la partie de la polarisation parallèle qui perpendiculaire au mur
        pola_parallel_normal = np.dot(np.dot(pola_parallel, wall.plane.normal_vector), wall.plane.normal_vector)
        #modification de la polarisation parallèle pour qu'elle reste perpendiculaire au vecteur d'onde
        pola_parallel = pola_parallel-np.dot(2,pola_parallel_normal)
        self.polarisation = np.dot(gamma_wall_perp, pola_perp) + np.dot(gamma_wall_para,pola_parallel)
        return 0
