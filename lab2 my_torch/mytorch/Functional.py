import numpy as np
from .Modules import Module


class Sigmoid(Module):

    def forward(self, x):
        """Forward propagation of Sigmoid.

        Args:
            x: input of shape (N, L_in).
        Returns:
            out: output of shape (N, L_out).
        """

        self.x = x

        return 1/(1+np.exp(-x))

    def backward(self, dy):
        """Backward propagation of Sigmoid.

        Args:
            dy: output delta of shape (N, L_out).
        Returns:
            dx: input delta of shape (N, L_in).
        """

        return dy * np.exp(-self.x)/((1+np.exp(-self.x))**2)


class ReLU(Module):

    def forward(self, x):
        """Forward propagation of ReLU.

        Args:
            x: input of shape (N, L_in).
        Returns:
            out: output of shape (N, L_out).
        """

        self.x = x

        return np.where(x > 0, x, 0)

    def backward(self, dy):
        """Backward propagation of ReLU.

        Args:
            dy: output delta of shape (N, L_out).
        Returns:
            dx: input delta of shape (N, L_in).
        """

        dy[self.x < 0] = 0

        return dy


class argmax(Module):

    def forward(self, x):
        """Forward propagation of ReLU.

        Args:
            x: input of shape (N, L_in).
        Returns:
            out: output of shape (N, 1).
        """
        self.x = x
        self.out = np.argmax(x, axis=1).reshape(-1, 1) - 1

        return self.out

    def backward(self, dy):
        """Backward propagation of Sigmoid.

        Args:
            dy: output delta of shape (N, 1).
        Returns:
            dx: input delta of shape (N, L_in).
        """
        dy = np.zeros_like(self.x)
        for i in range(self.x.shape[0]):
            dy[i][self.out[i]] = 1

        return dy


class Loss:
    """
    Usage:
        >>> criterion = Loss(n_classes)
        >>> ...
        >>> for epoch in n_epochs:
        ...     ...
        ...     predict = model(x)
        ...     loss = criterion(probs, target)
        ...     model.backward(loss.backward())
        ...     ...
    """

    def __init__(self, n_classes):
        self.n_classes = n_classes

    def __call__(self, predict, targets):
        self.predict = predict
        self.targets = targets
        ...
        return self

    def backward(self):
        ...


class MSELoss(Loss):

    def __call__(self, predict, targets):
        """Forward propagation of MSELoss.

        Args:
            predict: input of shape (1).
            targets: input of shape (1).
        Returns:
            loss: output of shape (1).
        """
        self.x = predict
        self.y = targets
        self.loss = 0.5*np.mean((targets - predict)**2)

        return self

    def backward(self,):
        """
        Backward propagation of MSELoss.
        """

        if len(self.x.shape) < 2:
            self.x = np.expand_dims(self.x, -1)
        if len(self.y.shape) < 2:
            self.y = np.expand_dims(self.y, -1)

        dy = self.x - self.y

        return dy
