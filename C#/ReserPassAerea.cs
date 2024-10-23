using System;
using System.Collections.Generic;

// Classe para representar um passageiro
class Passageiro
{
    public string Nome { get; set; }
    public string Sobrenome { get; set; }
    public string NumeroPassaporte { get; set; }

    // Construtor
    public Passageiro(string nome, string sobrenome, string numeroPassaporte)
    {
        Nome = nome;
        Sobrenome = sobrenome;
        NumeroPassaporte = numeroPassaporte;
    }

    // Método para exibir informações do passageiro
    public void ExibirInformacoes()
    {
        Console.WriteLine($"Nome: {Nome} {Sobrenome}, Número do Passaporte: {NumeroPassaporte}");
    }
}

// Classe para representar um voo
class Voo
{
    public string NumeroVoo { get; set; }
    public string Origem { get; set; }
    public string Destino { get; set; }
    public int Capacidade { get; set; }
    public List<Passageiro> Passageiros { get; set; }

    // Construtor
    public Voo(string numeroVoo, string origem, string destino, int capacidade)
    {
        NumeroVoo = numeroVoo;
        Origem = origem;
        Destino = destino;
        Capacidade = capacidade;
        Passageiros = new List<Passageiro>();
    }

    // Método para reservar assento para um passageiro
    public bool ReservarAssento(Passageiro passageiro)
    {
        if (Passageiros.Count < Capacidade)
        {
            Passageiros.Add(passageiro);
            return true;
        }
        else
        {
            Console.WriteLine("Não há mais assentos disponíveis neste voo.");
            return false;
        }
    }

    // Método para exibir informações do voo
    public void ExibirInformacoes()
    {
        Console.WriteLine($"Número do Voo: {NumeroVoo}, Origem: {Origem}, Destino: {Destino}, Capacidade: {Capacidade}, Assentos Disponíveis: {Capacidade - Passageiros.Count}");
    }

    // Método para exibir informações dos passageiros no voo
    public void ExibirPassageiros()
    {
        Console.WriteLine($"Passageiros no Voo {NumeroVoo}:");
        foreach (var passageiro in Passageiros)
        {
            passageiro.ExibirInformacoes();
        }
    }
}

class Program
{
    static void Main(string[] args)
    {
        // Criando alguns voos
        Voo voo1 = new Voo("AA123", "Nova York", "Los Angeles", 200);
        Voo voo2 = new Voo("BB456", "Paris", "Londres", 150);

        // Criando alguns passageiros
        Passageiro passageiro1 = new Passageiro("John", "Doe", "ABC123");
        Passageiro passageiro2 = new Passageiro("Jane", "Smith", "DEF456");

        // Reservando assentos nos voos
        voo1.ReservarAssento(passageiro1);
        voo1.ReservarAssento(passageiro2);
        voo2.ReservarAssento(passageiro2);

        // Exibindo informações dos voos e passageiros
        voo1.ExibirInformacoes();
        voo1.ExibirPassageiros();
        voo2.ExibirInformacoes();
        voo2.ExibirPassageiros();
    }
}