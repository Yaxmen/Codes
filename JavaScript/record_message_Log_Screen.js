(function executeRule(current, previous /*null when async*/ ) {

    //Escreva uma mensagem de log de nível de informação para registrar o endereço de e-mail do Solicitado
    gs.info("Requested for's email in: " + current.u_requested_for.email);

    //Escreva uma mensagem informativa na página mostrando o número do funcionário solicitado
    gs.addInfoMessage("Requested for's employee number is " + current.u_requested_for.employee_number);

    //Escreva uma mensagem informativa para a página se o usuário conectado no momento tiver a função de administrador
    if (gs.hasRole("admin")) {
        gs.addInfoMessage("currently logged in user has the admin role.");
    }

})(current, previous);