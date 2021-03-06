# plots.py
from __future__ import division
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

import numpy as np
from numpy import array as arr
from scipy.interpolate import interp1d
from scipy.linalg import solve
import matplotlib.pyplot as plt
from matplotlib.axis import Axis

from solutions import ode_fe, cheb
from tridiag import tridiag


def tridiagonal_approach():
	epsilon, alpha, beta = .02, 2., 4.
	# N = number of subintervals or finite elements

	def AnalyticSolution(x,alpha, beta,epsilon):
		out = alpha+x+(beta-alpha-1.)*(np.exp(x/epsilon) -1.)/(np.exp(1./epsilon) -1.)
		return out

	def matrix_diagonals(N):
		x = np.linspace(0,1,N+1)**(1.) # N+1 = number of grid points
		h = np.diff(x)
		b, f = np.zeros(N+1), np.zeros(N+1)
		a, c= np.zeros(N), np.zeros(N)
		b[0], b[N] = 1., 1.
		f[0], f[N] = alpha, beta
		# i = 0 to N-2
		b[1:N] = -epsilon*(1./h[0:N-1] + 1./h[1:N])
		f[1:N] = -.5*(h[0:N-1] + h[1:N])
		c[1:N] = epsilon/h[1:N] - .5
		a[0:N-1] = epsilon/h[0:N-1] + .5
		return a, b, c, f, x

	n = [2**i for i in range(4,22)]

	max_error_fe = [10]*(len(n))
	h = [1./num for num in n]
	for j in range(len(n)):
		a, b, c, f, x = matrix_diagonals(n[j])
		numerical_soln = tridiag(a,b,c,f)
		analytic_soln = AnalyticSolution(x, alpha, beta,epsilon)
		max_error_fe[j] = np.max(np.abs(numerical_soln - analytic_soln))

	n2 = [2*i for i in range(4,50)]
	max_error_cheb = [10]*len(n2)
	for j in range(len(n2)):
		N = n2[j]
		D,x = cheb(N)
		M = 4*epsilon*D.dot(D) -2.*D
		M[0] = 0.
		M[-1] = 0.
		M[0,0] = 1.
		M[-1,-1] = 1.

		F = -np.ones(len(x))
		F[0] = 4    # beta
		F[-1] = 2   # alpha

		cheb_sol = solve(M,F)
		analytic_soln = AnalyticSolution((x+1.)/2., alpha, beta,epsilon)
		max_error_cheb[j] = np.max(np.abs(cheb_sol - analytic_soln))

	plt.loglog(n2,max_error_cheb,'-b',linewidth=2.,label='Chebychev Error')

	plt.loglog(n,max_error_fe,'-k',linewidth=2.)
	plt.xlabel('$n$',fontsize=16)
	plt.ylabel('$E(n)$',fontsize=16)
	# plt.savefig("FEM_error_2nd_order.pdf")
	plt.show()
	plt.clf()


def basis_functions_plot():
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# ax = fig.add_axes([-.1,1.1, -.1,1.1])

	# Basis function phi_0
	x, y = arr([0,.2,.4,1.]), arr([1.,0.,0.,0.])
	ax.plot(x,y,'-k',linewidth=2.0)
	ax.text(0.,1.02,r"$\phi_0$",fontsize=18)

	# Basis function phi_1
	x, y = arr([0,.2,.4,1.]), arr([0.,1.,0.,0.])
	ax.plot(x,y,color='g',lw=2.0)
	ax.text(0.2,1.02,r"$\phi_1$",fontsize=18)

	# Basis function phi_2
	x, y = arr([0,.2,.4,.6,1.]), arr([0.,0.,1.,0.,0.])
	ax.plot(x,y,color='r',lw=2.0)
	ax.text(0.4,1.02,r"$\phi_2$",fontsize=18)

	# Basis function phi_3
	x, y = arr([0,.4,.6,.8,1.]), arr([0.,0.,1.,0.,0.])
	ax.plot(x,y,'-m',linewidth=2.0)
	ax.text(0.6,1.02,r"$\phi_3$",fontsize=18)

	# Basis function phi_4
	x, y = arr([0,.6,.8,1.]), arr([0.,0.,1.,0.])
	ax.plot(x,y,'-b',linewidth=2.0)
	ax.text(0.8,1.02,r"$\phi_4$",fontsize=18)

	# Basis function phi_5
	x, y = arr([0,.8,1.]), arr([0.,0.,1.])
	ax.plot(x,y,'-c',linewidth=2.0)
	ax.text(1.,1.02,r"$\phi_5$",fontsize=18)

	ax.set_ylim(-.1,1.1)
	ax.set_xlim(-.1,1.1)
	plt.xticks(np.linspace(0.,1.,6),['$x_0$','$x_1$','$x_2$','$x_3$','$x_4$','$x_5$'],fontsize=18)
	# print Axis.get_majorticklabels(plt.axis)
	# plt.savefig("basis_functions.pdf")
	plt.clf()



def one_basis_function_plot():
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# ax = fig.add_axes([-.1,1.1, -.1,1.1])

	# Basis function phi_3
	x, y = arr([0,.4,.6,.8,1.]), arr([0.,0.,1.,0.,0.])
	ax.plot(x,y,'-m',linewidth=2.0)
	ax.text(0.6,1.02,r"$\phi_3$",fontsize=18)


	ax.set_ylim(-.1,1.1)
	ax.set_xlim(-.1,1.1)
	# plt.xticks(np.linspace(0.,1.,6),['$x_0$','$x_1$','$x_2$','$x_3$','$x_4$','$x_5$'],fontsize=18)
	plt.xticks(arr([.4,.6,.8]),['$x_2$','$x_3$','$x_4$'],fontsize=18)
	# print Axis.get_majorticklabels(plt.axis)
	# plt.savefig("one_basis_function.pdf")

	# plt.show()
	plt.clf()


if __name__ == "__main__":
	# basis_functions_plot()
	# one_basis_function_plot()
	tridiagonal_approach()
