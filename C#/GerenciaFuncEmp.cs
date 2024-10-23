using System;
using System.Collections.Generic;

// Classe base para representar um funcionário
class Funcionario
{
    public string Nome { get; set; }
    public int Idade { get; set; }
    public double Salario { get; set; }

    // Construtor
    public Funcionario(string nome, int idade, double salario)
    {
        Nome = nome;
        Idade = idade;
        Salario = salario;
    }

    // Método para calcular bônus
    public virtual double CalcularBonus()
    {
        return Salario * 0.1; // 10% do salário como bônus padrão
    }

    // Método para exibir informações do funcionário
    public virtual void ExibirInformacoes()
    {
        Console.WriteLine($"Nome: {Nome}, Idade: {Idade}, Salário: {Salario:C}, Bônus: {CalcularBonus():C}");
    }
}

// Classe para representar um funcionário em tempo integral
class FuncionarioTempoIntegral : Funcionario
{
    // Construtor
    public FuncionarioTempoIntegral(string nome, int idade, double salario) : base(nome, idade, salario)
    {
    }

    // Sobrescreve o método CalcularBonus para funcionários em tempo integral
    public override double CalcularBonus()
    {
        return Salario * 0.15; // 15% do salário como bônus para funcionários em tempo integral
    }
}

// Classe para representar um funcionário contratado por hora
class FuncionarioPorHora : Funcionario
{
    public int HorasTrabalhadas { get; set; }

    // Construtor
    public FuncionarioPorHora(string nome, int idade, double salario, int horasTrabalhadas) : base(nome, idade, salario)
    {
        HorasTrabalhadas = horasTrabalhadas;
    }

    // Sobrescreve o método CalcularBonus para funcionários contratados por hora
    public override double CalcularBonus()
    {
        return Salario * 0.05 * HorasTrabalhadas; // 5% do salário multiplicado pelo número de horas trabalhadas como bônus
    }

    // Sobrescreve o método para exibir informações do funcionário contratado por hora
    public override void ExibirInformacoes()
    {
        Console.WriteLine($"Nome: {Nome}, Idade: {Idade}, Salário: {Salario:C}, Horas Trabalhadas: {HorasTrabalhadas}, Bônus: {CalcularBonus():C}");
    }
}

class Program
{
    static void Main(string[] args)
    {
        // Criando uma lista de funcionários
        List<Funcionario> funcionarios = new List<Funcionario>
        {
            new FuncionarioTempoIntegral("João", 35, 3000),
            new FuncionarioPorHora("Maria", 28, 20, 160),
            new FuncionarioTempoIntegral("Carlos", 40, 4000)
        };

        // Exibindo informações e bônus de cada funcionário
        foreach (var funcionario in funcionarios)
        {
            funcionario.ExibirInformacoes();
        }
    }
}