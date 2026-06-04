import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

model = nn.Sequential(
    nn.Linear(20, 64),
    nn.ReLU(),
    nn.Linear(64, 1),
)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

# Datos: train pequeño, val grande → overfitting intencional
torch.manual_seed(42)
X_train = torch.randn(50, 20)
y_train = torch.randn(50, 1)
X_val   = torch.randn(500, 20)
y_val   = torch.randn(500, 1)

writer = SummaryWriter("runs/overfitting_demo")

for step in range(300):
    model.train()
    optimizer.zero_grad()
    loss_train = criterion(model(X_train), y_train)
    loss_train.backward()
    optimizer.step()

    model.eval()
    with torch.no_grad():
        loss_val = criterion(model(X_val), y_val)

    writer.add_scalar("loss/train", loss_train.item(), step)
    writer.add_scalar("loss/val",   loss_val.item(),   step)

writer.close()
print("Listo. Corre: tensorboard --logdir=runs")
