let get_total_to_approve =  () => {
    $('document').ready(function(){
        let note = $('.total-to-approve')
        function getTotalToApprove(){
            $.ajax({
                url: '/system_core_1/get_total_to_approve/',
                method: 'GET',
                contentTpe: 'application/json',
                success: function(data){
                    if(data){
                        note.text(`${data.total_to_approve}`)
                    }
                }
            })
        }
        getTotalToApprove()
        setInterval(getTotalToApprove, 5 * 60 * 1000)
    });
}
get_total_to_approve()