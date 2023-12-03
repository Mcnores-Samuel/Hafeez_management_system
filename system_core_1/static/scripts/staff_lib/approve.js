let get_approved =  () => {
    $('document').ready(function(){
        let note = $('.approved-notice')
        function getApproved(){
            $.ajax({
                url: '/system_core_1/get_approved/',
                method: 'GET',
                contentTpe: 'application/json',
                success: function(data){
                    if(data){
                        note.text(`${data.total_approved}`)
                    }
                }
            })
        }
        getApproved()
        setInterval(getApproved, 5 * 60 * 1000)
    });
}
get_approved()