import torch, time, gc

# Timing utilities
start_time = None


def start_timer():
    global start_time
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.reset_max_memory_allocated()
    torch.cuda.synchronize()
    start_time = time.time()


def end_timer_and_return(local_msg):
    torch.cuda.synchronize()
    end_time = time.time()
    elapsed = end_time - start_time
    max_memory = torch.cuda.max_memory_allocated()
    print("\n" + local_msg)
    print("Total execution time = {:.3f} sec".format(elapsed))
    print("Max memory used by tensors = {} bytes".format(max_memory))
    return elapsed, max_memory


def make_model(in_size, out_size, num_layers):
    layers = []
    for _ in range(num_layers - 1):
        layers.append(torch.nn.Linear(in_size, in_size))
        layers.append(torch.nn.ReLU())
    layers.append(torch.nn.Linear(in_size, out_size))
    return torch.nn.Sequential(*tuple(layers)).cuda()


batch_size = 512  # Try, for example, 128, 256, 513.
in_size = 4096
out_size = 4096
num_layers = 3
num_batches = 50
epochs = 3

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.set_default_device(device)

# Creates data in default precision.
# The same data is used for both default and mixed precision trials below.
# You don't need to manually change inputs' ``dtype`` when enabling mixed precision.
data = [torch.randn(batch_size, in_size) for _ in range(num_batches)]
targets = [torch.randn(batch_size, out_size) for _ in range(num_batches)]

loss_fn = torch.nn.MSELoss().cuda()

# Run FP32 training (baseline)
print("=" * 60)
print("Running FP32 (baseline) training...")
print("=" * 60)
net = make_model(in_size, out_size, num_layers)
opt = torch.optim.SGD(net.parameters(), lr=0.001)

start_timer()
for epoch in range(epochs):
    for input, target in zip(data, targets):
        output = net(input)
        loss = loss_fn(output, target)
        loss.backward()
        opt.step()
        opt.zero_grad()
fp32_time, fp32_memory = end_timer_and_return("FP32 precision:")

# Run AMP training
print("\n" + "=" * 60)
print("Running AMP (mixed precision) training...")
print("=" * 60)
net = make_model(in_size, out_size, num_layers)
opt = torch.optim.SGD(net.parameters(), lr=0.001)
scaler = torch.amp.GradScaler("cuda")

start_timer()
for epoch in range(epochs):
    for input, target in zip(data, targets):
        with torch.autocast(device_type=device, dtype=torch.float16):
            output = net(input)
            loss = loss_fn(output, target)
        scaler.scale(loss).backward()
        scaler.step(opt)
        scaler.update()
        opt.zero_grad()
amp_time, amp_memory = end_timer_and_return("AMP precision:")

# Display comparison results
print("\n" + "=" * 60)
print("PERFORMANCE COMPARISON")
print("=" * 60)
print(f"FP32 Time:   {fp32_time:.3f} sec")
print(f"AMP Time:    {amp_time:.3f} sec")
print(f"Speedup:     {fp32_time/amp_time:.2f}x")
print()
print(f"FP32 Memory: {fp32_memory:,} bytes ({fp32_memory/1024**2:.1f} MB)")
print(f"AMP Memory:  {amp_memory:,} bytes ({amp_memory/1024**2:.1f} MB)")
print(f"Memory saved: {(1 - amp_memory/fp32_memory)*100:.1f}%")
print("=" * 60)
