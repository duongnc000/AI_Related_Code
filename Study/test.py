import torch

# Create some data and labels
x = torch.randn(3, 3, requires_grad=True)  # Input tensor with requires_grad=True
y = torch.randn(3, 3)  # Target tensor (no need for requires_grad)

print(x)  # Print the input tensor
print(y)  # Print the target tensor

# Define a simple loss function
loss = torch.sum(x ** 2)  # Example loss function: L2 loss (sum of squares)

# Backpropagation step
loss.backward()  # Computes the gradient of loss with respect to x

# Print loss
print(loss.item())  # This will print the scalar loss value

# Print gradients
print(x.grad)  # This will print the gradient of the loss with respect to x