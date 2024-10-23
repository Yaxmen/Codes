using System;
using System.Collections.Generic;

// Classe para representar um produto
class Produto
{
    public int Id { get; set; }
    public string Nome { get; set; }
    public double Preco { get; set; }
    public int QuantidadeEmEstoque { get; set; }

    // Construtor
    public Produto(int id, string nome, double preco, int quantidadeEmEstoque)
    {
        Id = id;
        Nome = nome;
        Preco = preco;
        QuantidadeEmEstoque = quantidadeEmEstoque;
    }

    // Método para exibir informações do produto
    public void ExibirInformacoes()
    {
        Console.WriteLine($"ID: {Id}, Nome: {Nome}, Preço: {Preco:C}, Quantidade em Estoque: {QuantidadeEmEstoque}");
    }
}

// Classe para representar uma transação de entrada/saída de produtos
class Transacao
{
    public enum TipoTransacao { Entrada, Saida }

    public TipoTransacao Tipo { get; set; }
    public Produto Produto { get; set; }
    public int Quantidade { get; set; }
    public DateTime Data { get; set; }

    // Construtor
    public Transacao(TipoTransacao tipo, Produto produto, int quantidade)
    {
        Tipo = tipo;
        Produto = produto;
        Quantidade = quantidade;
        Data = DateTime.Now;
    }

    // Método para exibir informações da transação
    public void ExibirInformacoes()
    {
        string tipo = Tipo == TipoTransacao.Entrada ? "Entrada" : "Saída";
        Console.WriteLine($"Tipo: {tipo}, Produto: {Produto.Nome}, Quantidade: {Quantidade}, Data: {Data}");
    }
}

// Classe para representar o estoque
class Estoque
{
    private List<Transacao> transacoes;

    // Construtor
    public Estoque()
    {
        transacoes = new List<Transacao>();
    }

    // Método para adicionar uma transação ao estoque
    public void AdicionarTransacao(Transacao transacao)
    {
        transacoes.Add(transacao);

        // Atualiza a quantidade em estoque do produto
        if (transacao.Tipo == Transacao.TipoTransacao.Entrada)
        {
            transacao.Produto.QuantidadeEmEstoque += transacao.Quantidade;
        }
        else
        {
            transacao.Produto.QuantidadeEmEstoque -= transacao.Quantidade;
        }
    }

    // Método para exibir todas as transações do estoque
    public void ExibirTransacoes()
    {
        Console.WriteLine("Transações de Estoque:");
        foreach (var transacao in transacoes)
        {
            transacao.ExibirInformacoes();
        }
    }
}

class Program
{
    static void Main(string[] args)
    {
        // Criando alguns produtos
        Produto produto1 = new Produto(1, "Camiseta", 29.99, 50);
        Produto produto2 = new Produto(2, "Calça Jeans", 59.99, 30);

        // Criando o estoque
        Estoque estoque = new Estoque();

        // Adicionando transações de entrada/saída de produtos ao estoque
        Transacao entrada1 = new Transacao(Transacao.TipoTransacao.Entrada, produto1, 20);
        Transacao saida1 = new Transacao(Transacao.TipoTransacao.Saida, produto1, 10);
        Transacao entrada2 = new Transacao(Transacao.TipoTransacao.Entrada, produto2, 15);

        // Adicionando transações ao estoque
        estoque.AdicionarTransacao(entrada1);
        estoque.AdicionarTransacao(saida1);
        estoque.AdicionarTransacao(entrada2);

        // Exibindo todas as transações do estoque
        estoque.ExibirTransacoes();

        // Exibindo informações atualizadas dos produtos após as transações
        produto1.ExibirInformacoes();
        produto2.ExibirInformacoes();
    }
}