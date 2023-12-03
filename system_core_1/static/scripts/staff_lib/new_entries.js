let get_new_entries =  () => {
    $('document').ready(function(){
        let note = $('.new-entries-notice')
        function getNewEntries(){
            $.ajax({
                url: '/system_core_1/get_new_entries_total/',
                method: 'GET',
                contentTpe: 'application/json',
                success: function(data){
                    if(data){
                        note.text(`${data.total_new_entries}`)
                    }
                }
            })
        }
        getNewEntries()
        setInterval(getNewEntries, 5 * 60 * 1000)
    });
}
get_new_entries()