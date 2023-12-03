let get_total_rejected =  () => {
    $('document').ready(function(){
        let note = $('.total-rejected')
        function getTotalRejected(){
            $.ajax({
                url: '/system_core_1/total_rejected/',
                method: 'GET',
                contentTpe: 'application/json',
                success: function(data){
                    if(data){
                        note.text(`${data.total_rejected}`)
                    }
                }
            })
        }
        getTotalRejected()
        setInterval(getTotalRejected, 5 * 60 * 1000)
    });
}
get_total_rejected()