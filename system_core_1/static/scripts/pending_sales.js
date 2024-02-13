let get_pending_sales =  () => {
    $('document').ready(function(){
        let note = $('.pending-sales-notice')
        function getPendingSales(){
            $.ajax({
                url: '/system_core_1/total_pending_sales/',
                method: 'GET',
                contentTpe: 'application/json',
                success: function(data){
                    if(data){
                        note.text(`${data.total}`)
                    }
                }
            })
        }
        getPendingSales()
        setInterval(getPendingSales, 5 * 60 * 1000)
    });
}

get_pending_sales()