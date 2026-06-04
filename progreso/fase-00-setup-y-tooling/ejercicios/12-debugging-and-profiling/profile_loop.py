import torch
import torch.nn as nn
import cProfile

model = nn.Sequential(
    nn.Linear(784, 512),
    nn.ReLU(),
    nn.Linear(512, 256),
    nn.ReLU(),
    nn.Linear(256, 10),
)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

def training_loop():
    for _ in range(100):
        x = torch.randn(64, 784)
        target = torch.randint(0, 10, (64,))
        optimizer.zero_grad()
        output = model(x)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

cProfile.run("training_loop()", sort="cumtime")
