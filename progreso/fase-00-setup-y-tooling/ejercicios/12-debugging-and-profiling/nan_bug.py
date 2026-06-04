import torch
import torch.nn as nn
import sys
sys.path.insert(0, ".")
from debug_tools import detect_nan, debug_print

class ModelConBug(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 5)

    def forward(self, x):
        out = self.fc(x)
        out = out / (out - out)  # bug: división por cero → NaN
        return out

model = ModelConBug()
x = torch.randn(4, 10)
target = torch.randint(0, 5, (4,))
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

optimizer.zero_grad()
output = model(x)
debug_print("output", output)
loss = criterion(output, target)
print(f"Loss: {loss.item()}")
detect_nan(model, loss, step=1)
