import tensorflow as tf

# Create a Constant op that produces a 1x2 matrix.  The op is
# added as a node to the default graph.

matrix1 = tf.constant([[3., 3.]])
matrix2 = tf.constant([[2.],[1.]])

# Create a Matmul op that takes 'matrix1' and 'matrix2' as inputs.
product = tf.matmul(matrix1, matrix2)

# Launch the default graph.
session = tf.Session()
result = session.run(product)
print(result)

session.close()




# Create a Variable, that will be initialized to the scalar value 0.
state = tf.Variable(0, name="counter")

# Create an Op to add one to `state`.

one = tf.constant(1)
new_value = tf.add(state, one)
update = tf.assign(state, new_value)

# Variables must be initialized by running an `init` Op after having
# launched the graph.  We first have to add the `init` Op to the graph.
init_op = tf.global_variables_initializer()

# Launch the graph and run the ops.
with tf.Session() as sess:
# Run the 'init'op
    sess.run(init_op)
  # Print the initial value of 'state'
    print(sess.run(state))
  # Run the op that updates 'state' and print 'state'.
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))

   
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)
output = tf.multiply(input1,input2)
# Launch the graph and run the ops.
with tf.Session() as sess:
    # Print the output
    print(sess.run([output],feed_dict={input1:[7.], input2:[2.]}))
                                   
