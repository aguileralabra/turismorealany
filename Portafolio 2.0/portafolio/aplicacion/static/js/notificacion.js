document.addEventListener('DOMContentLoaded', function()
{
    if(Notification.permission != "granted")
        Notification.requestPermission();
})

// funcion para llamar a una notificacion

function notificar(titulo, mensaje, url)
{
    var notificacion = new Notification (
        titulo,
        {
            icon                     : 'static/img/logo.PNG',
            body                     : mensaje,
            requireInteraction       : false
        });
    notificacion.onclick = function()
    {
        window.open(url);
    }
}
//LLAMAR A LA NOTIFIACAION
setTimeout(function()
{
    var titulo = "Turismo Real";
    var mensaje = "Bienvenido, te recordar el paso a paso por covid-19";
    var url = "https://www.gob.cl/pasoapaso/";
    notificar(titulo, mensaje, url);
}, 2000)