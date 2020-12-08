if ('serviceWorker' in navigator) { 
    navigator.serviceWorker.register('sw.js',{ scope: '../'}).then(function(reg){
        console.log('Registro-exitoso. El alcance es: ' + reg.scope);
    }) .catch(function(error) {
        console.log('Error al registrar' + error);
    });
}