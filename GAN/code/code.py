import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from time import time

import sys, os
sys.path.insert(0, '../../helper_libraries/')
from helper_functions import get_h_m_s, calculate_ETC

class PlotGraph():
	def plot_generated_vs_real_data(self, G, R, iteration_number):
		x, y = G[:, 0].tolist(), G[:, 1].tolist()
		plt.plot(x, y, 'ro', label='generated data')
		x, y = R[:, 0].tolist(), R[:, 1].tolist()
		plt.plot(x, y, 'go', label='actual data data')
		plt.legend()
		plt.savefig('../data/plots_for_generated_vs_actual/%s.png' %(iteration_number))
		plt.close()

	def plot_loss(self, g_loss, d_loss):
		x = range(0, len(g_loss))
		plt.plot(x, g_loss, 'r-', label = 'generator loss')
		plt.plot(x, d_loss, 'r-', label = 'discriminator loss')
		plt.legend()
		plt.savefig('../data/%s.png' %('loss'))
		plt.close()


def get_y(x):
    return  np.sin(x)

def sample_Z(n=10000, scale=300):
 	data = []
	x = scale*(np.random.random_sample((n,))-0.5)
	y = scale*(np.random.random_sample((n,))-0.5)
 	for xi, yi in zip(x, y):
 		data.append([xi, yi])
 	return np.array(data)


def sample_data(n=10000, scale=100):
    data = []

    x = scale*(np.random.random_sample((n,))-0.5)

    for i in range(n):
        yi = get_y(x[i])
        data.append([x[i], yi])

    return np.array(data)

def generator(Z, hsize=[16, 16], reuse=False):
    with tf.variable_scope("GAN/Generator",reuse=reuse):
        h1 = tf.layers.dense(Z,hsize[0],activation=tf.nn.leaky_relu)
        h2 = tf.layers.dense(h1,hsize[1],activation=tf.nn.leaky_relu)
        out = tf.layers.dense(h2, 2)

    return out

def discriminator(X, hsize=[16, 16], reuse=False):
    with tf.variable_scope("GAN/Discriminator",reuse=reuse):
        h1 = tf.layers.dense(X, hsize[0],activation=tf.nn.leaky_relu)
        h2 = tf.layers.dense(h1, hsize[1],activation=tf.nn.leaky_relu)
        h3 = tf.layers.dense(h2, 2)
        out = tf.layers.dense(h3, 1)

    return out, h3

X = tf.placeholder(tf.float32,[None, 2]) ## actual distribution
Z = tf.placeholder(tf.float32,[None, 2]) ## random input
G_sample = generator(Z)
r_logits, r_rep = discriminator(X)
f_logits, g_rep = discriminator(G_sample,reuse=True)

disc_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=r_logits,labels=tf.ones_like(r_logits)) + tf.nn.sigmoid_cross_entropy_with_logits(logits=f_logits,labels=tf.zeros_like(f_logits)))
gen_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=f_logits,labels=tf.ones_like(f_logits)))

gen_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="GAN/Generator")
disc_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="GAN/Discriminator")

gen_step = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(gen_loss,var_list = gen_vars)

disc_step = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(disc_loss,var_list = disc_vars)

start = time()
total = 100001
batch_size = 1000
dloss_history = []
gloss_history = []

plot_graph = PlotGraph()

with tf.Session() as sess:
	sess.run(tf.initializers.global_variables())
	for i in range(total):
		X_batch = sample_data(n=batch_size)
		Z_batch = sample_Z(n=batch_size)
		_, dloss = sess.run([disc_step, disc_loss], feed_dict={X: X_batch, Z: Z_batch})
		_, gloss, Generated_batch = sess.run([gen_step, gen_loss, G_sample], feed_dict={Z: Z_batch})

		if i % 10 == 0:
			dloss_history.append(dloss)
			gloss_history.append(gloss)
		if i% 1000 == 0:
			### plot generated vs actual sample
			plot_graph.plot_generated_vs_real_data(Generated_batch, X_batch, i)
		time_elapsed = time() - start
		print "%s/%s dloss :: %s, gloss :: %s, time elapsed :: %s, time remaining :: %s" %(i, total, dloss, gloss, get_h_m_s(time_elapsed), get_h_m_s(calculate_ETC(time_elapsed, i +1, total - i -1)))
plot_graph.plot_loss(gloss_history, dloss_history)
