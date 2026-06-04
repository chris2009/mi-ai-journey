import torch
import torch.nn as nn

model = nn.Linear(10, 5)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for step in range(10):
    x = torch.randn(4, 10)
    target = torch.randint(0, 5, (4,))
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()

    if step == 3:   # ← para en el step 3
        breakpoint()
