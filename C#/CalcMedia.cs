using System;

class Program
{
    static void Main(string[] args)
    {
        // Lista de números
        double[] numeros = { 10.5, 20.3, 15.7, 30.8, 25.2 };

        // Chama a função para calcular a média
        double media = CalcularMedia(numeros);

        // Exibe o resultado
        Console.WriteLine("A média dos números é: " + media);
    }

    // Função para calcular a média
    static double CalcularMedia(double[] numeros)
    {
        double soma = 0;

        // Soma todos os números na lista
        foreach (double num in numeros)
        {
            soma += num;
        }

        // Calcula a média
        double media = soma / numeros.Length;

        return media;
    }
}