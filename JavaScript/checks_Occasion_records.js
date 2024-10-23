//O método GlideSystem gs.setProperty() define o valor de uma propriedade do sistema de um script do lado do servidor. Use gs.setProperty com EXTREMO cuidado. Ele causa liberações de cache que podem levar a problemas de desempenho durante a descarga. Os valores de propriedade devem ser definidos manualmente.

// recuperar o valor da propriedade x_58872_needit.daysNotice Application
var daysNotice = gs.getProperty("x_58872_needit.daysNotice");

// obter a data de hoje e adicionar o número de dias da propriedade
var today = new GlideDataTime();
var compareDate = today.addDaysLocalTime(daysNotice);

// obter o mês e o dia para o compareDate
var month = compareDate.getMonthLocalTime();
var day = compareDate.getDayOfMonthLocalTime();

// consultar a tabela Ocasião para dias especiais que correspondem à compareDate e não estão marcados como particulares
var upcomingOccasion = new GlideRecord('x_58872_needit_occasions');
upcomingOccasion.addQuery('occasion_month', month);
upcomingOccasion.addQuery('occasion_day',day);
upcomingOccasion.addQuery('private',false);
upcomingOccasion.query();

// criar um evento para cada registro encontrado
while(upcomingOccasion.next()){
    gs.info("Occasion record: " + upcomingOccasion.number);
    gs.eventQueue('x_58872_needit.employeeOccasion',upcomingOccasionm,upcomingOccasion.number,upcomingOccasion.u_employee.name,'my_queue');
}