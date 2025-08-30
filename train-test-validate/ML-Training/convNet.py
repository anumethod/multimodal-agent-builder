// lets use an example fully-connected 2-layer ReLU net
var layer_defs = [];
layer_defs.push({type:'input', out_sx:24, out_sy:24, out_depth:1});
layer_defs.push({type:'fc', num_neurons:20, activation:'relu'});
layer_defs.push({type:'fc', num_neurons:20, activation:'relu'});
layer_defs.push({type:'softmax', num_classes:10});

// below fill out the trainer specs you wish to evaluate, and give them names for legend
var LR = 0.01; // learning rate
var BS = 8; // batch size
var L2 = 0.001; // L2 weight decay
nets = [];
trainer_defs = [];
trainer_defs.push({learning_rate:10*LR, method: 'sgd', momentum: 0.0, batch_size:BS, l2_decay:L2});
trainer_defs.push({learning_rate:LR, method: 'sgd', momentum: 0.9, batch_size:BS, l2_decay:L2});
trainer_defs.push({learning_rate:LR, method: 'adagrad', eps: 1e-6, batch_size:BS, l2_decay:L2});
trainer_defs.push({learning_rate:LR, method: 'windowgrad', eps: 1e-6, ro: 0.95, batch_size:BS, l2_decay:L2});
trainer_defs.push({learning_rate:1.0, method: 'adadelta', eps: 1e-6, ro:0.95, batch_size:BS, l2_decay:L2});
trainer_defs.push({learning_rate:LR, method: 'nesterov', momentum: 0.9, batch_size:BS, l2_decay:L2});

// names for all trainers above
legend = ['sgd', 'sgd+momentum', 'adagrad', 'windowgrad', 'adadelta', 'nesterov'];
