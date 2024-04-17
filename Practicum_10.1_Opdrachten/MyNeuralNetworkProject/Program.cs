using System;

public class NeuralNetwork {
    private int inputNodes;
    private int hiddenNodes;
    private int outputNodes;
    private double[,] inputToHiddenWeights;
    private double[,] hiddenToOutputWeights;

    public NeuralNetwork(int inputNodes, int hiddenNodes, int outputNodes) {
        this.inputNodes = inputNodes;
        this.hiddenNodes = hiddenNodes;
        this.outputNodes = outputNodes;

        inputToHiddenWeights = new double[inputNodes, hiddenNodes];
        hiddenToOutputWeights = new double[hiddenNodes, outputNodes];
        InitializeWeights(inputToHiddenWeights);
        InitializeWeights(hiddenToOutputWeights);
    }

    private void InitializeWeights(double[,] weights) {
        Random random = new Random();
        for (int i = 0; i < weights.GetLength(0); i++) {
            for (int j = 0; j < weights.GetLength(1); j++) {
                weights[i, j] = random.NextDouble() * 2 - 1; 
            }
        }
    }

    public double[] FeedForward(double[] input) {
        double[] hiddenOutputs = new double[hiddenNodes];
        double[] finalOutputs = new double[outputNodes];

        // Calculate the output of the hidden layer
        for (int i = 0; i < hiddenNodes; i++) {
            double sum = 0;
            for (int j = 0; j < inputNodes; j++) {
                sum += input[j] * inputToHiddenWeights[j, i];
            }
            hiddenOutputs[i] = Sigmoid(sum);
        }

        // Calculate the output of the output layer
        for (int i = 0; i < outputNodes; i++) {
            double sum = 0;
            for (int j = 0; j < hiddenNodes; j++) {
                sum += hiddenOutputs[j] * hiddenToOutputWeights[j, i];
            }
            finalOutputs[i] = Sigmoid(sum);
        }

        return finalOutputs;
    }

    private double Sigmoid(double x) {
        return 1 / (1 + Math.Exp(-x));
    }


// Train the network with given input-output pairs// Train the network with given input-output pairs
public void Train(double[,] inputs, double[,] outputs) {
    for (int i = 0; i < inputs.GetLength(0); i++) {
        double[] input = new double[inputNodes];
        double[] target = new double[outputNodes];
        double[] hiddenOutputs = new double[hiddenNodes]; // declare hiddenOutputs here

        // Load the input and target for this data point
        for (int j = 0; j < inputNodes; j++) {
            input[j] = inputs[i, j];
        }
        for (int j = 0; j < outputNodes; j++) {
            target[j] = outputs[i, j];
        }

        // Feedforward
        double[] output = FeedForward(input);

        // Calculate the error
        double[] outputError = new double[outputNodes];
        for (int j = 0; j < outputNodes; j++) {
            outputError[j] = target[j] - output[j];
        }

        // Print the predicted output
        Console.WriteLine("Predicted output: " + output[0]);

        // Update weights using error
        for (int j = 0; j < hiddenNodes; j++) {
            for (int k = 0; k < outputNodes; k++) {
                hiddenToOutputWeights[j, k] += outputError[k] * output[k] * (1 - output[k]) * hiddenOutputs[j];
            }
        }
        for (int j = 0; j < inputNodes; j++) {
            for (int k = 0; k < hiddenNodes; k++) {
                double sum = 0;
                for (int l = 0; l < outputNodes; l++) {
                    sum += outputError[l] * output[l] * (1 - output[l]) * hiddenToOutputWeights[k, l];
                }
                inputToHiddenWeights[j, k] += sum * input[j] * (1 - input[j]);
            }
        }
    }
}

    

}

class Program {
    static void Main(string[] args) {
        int inputNodes = 4;
        int hiddenNodes = 3;
        int outputNodes = 1;

        NeuralNetwork nn = new NeuralNetwork(inputNodes, hiddenNodes, outputNodes);

        // Sample input-output data
        double[,] inputs = { { 0, 0, 0, 0 }, { 0, 0, 1, 1 }, { 0, 1, 0, 1 }, { 1, 1, 1, 1 } };
        double[,] outputs = { { 0 }, { 1 }, { 1 }, { 0 } };

        // Train the network
        nn.Train(inputs, outputs);

        // Test the network with new input
        double[] testInput = { 1, 0, 1, 0 };
        double[] result = nn.FeedForward(testInput);

        Console.WriteLine("Output: " + result[0]);
    }
}
