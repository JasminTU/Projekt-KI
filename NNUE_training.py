import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Step 1: Data Preparation
# Assuming you have your dataset prepared with chess positions and evaluation scores

# Step 2: Neural Network Architecture
class NNUEModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NNUEModel, self).__init__()
        # - Linear and ClippedReLU clamp(0, 1)
        # - 2-4 layers
        self.L_0 = nn.Linear(input_size, hidden_size)
        self.l1 = nn.Linear(hidden_size * 2, hidden_size *2)
        self.l2 = nn.Linear(hidden_size * 2, output_size)

    # `stm` indicates the whether white is the side to move. 1 = true, 0 = false.
    def forward(self, white_features, black_features, stm):
        w = self.L_0(white_features) # white's perspective
        b = self.L_0(black_features) # black's perspective

        # Remember that we order the accumulators for 2 perspectives based on who is to move.
        # So we blend two possible orderings by interpolating between `stm` and `1-stm` tensors.
        accumulator = (stm * torch.cat([w, b], dim=1)) + ((1 - stm) * torch.cat([b, w], dim=1))

        # Run the linear layers and use clamp_ as ClippedReLU
        l1_x = torch.clamp(accumulator, 0.0, 1.0)
        l2_x = torch.clamp(self.l1(l1_x), 0.0, 1.0)
        return self.l2(l2_x)


# Step 3: Training Loop
def train_nnue_model(dataset, input_size, output_size, hidden_size, learning_rate, num_epochs, batch_size):
    model = NNUEModel(input_size, hidden_size, output_size)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)

    # Split dataset into training and validation sets
    train_ratio = 0.8
    train_size = int(train_ratio * len(dataset))
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, len(dataset) - train_size])

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Step 4: Training Process
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, data in enumerate(train_loader):
            inputs, labels = data

            optimizer.zero_grad()
            outputs = model(inputs)

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")

    # Step 5: Evaluation (on validation set)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size)
    with torch.no_grad():
        val_loss = 0.0
        for val_inputs, val_labels in val_loader:
            val_outputs = model(val_inputs)
            val_loss += criterion(val_outputs, val_labels).item()
        val_loss /= len(val_loader)
        print(f"Validation Loss: {val_loss:.4f}")

    # Step 6: Save trained model
    torch.save(model.state_dict(), "nnue_model.pth")


if __name__ == "__main__":
    # Example usage
    # Assuming you have 'dataset' as your prepared dataset and other relevant parameters
    dataset = None
    input_size = 64*64*5*2*2 # Tuple (our_king_sqare, Square, Figure, Color) --> 1 if true, 0 otherwise
    output_size = 1
    hidden_size = 4
    learning_rate = 0.001
    num_epochs = 10
    batch_size = 32

    train_nnue_model(dataset, input_size, output_size, hidden_size, learning_rate, num_epochs, batch_size)
