// setInterval(
    function job_state (task_id) {
        var taskID = task_id; 

        $.ajax({
            url: '/etl/'.concat(taskID),
            // url: '/c346dcc0-8766-4bc9-a511-b05be596a278',
            type: 'get',
            success: function(data) {
                
                // alert("ETL Job Submitted");
                if (data.job_state == "SUCCESS") {
                    clearTimeout(job_state)
                    document.getElementById("task_description").innerHTML = data.etl_info.description;
                    document.getElementById("task_status").innerHTML = data.job_state;
                    document.getElementById("progres_pic").innerHTML = "<img src='/static/loading/Done.png' style='width:100px;height:100px;'>";
                }
                else if (data.job_state == "FAILURE") {
                    clearTimeout(job_state)
                    document.getElementById("task_description").innerHTML = data.etl_info.description;
                    document.getElementById("task_status").innerHTML = data.job_state;
                    document.getElementById("progres_pic").innerHTML = "<img src='/static/loading/Done.png' style='width:100px;height:100px;'>";
                }
                else{
                    setTimeout(job_state, 1000, task_id);
                    document.getElementById("task_description").innerHTML = data.etl_info.description;
                    document.getElementById("task_status").innerHTML = data.job_state;
                    // document.getElementById("progres_pic").innerHTML = "<img src='https://media.giphy.com/media/feN0YJbVs0fwA/giphy.gif' style='width:100px;height:100px;'>";
                    document.getElementById("progres_pic").innerHTML = "<img src='https://media.giphy.com/media/sSgvbe1m3n93G/giphy.gif' style='width:100px;height:100px;'>";
                }
                
            },
            failure: function(data) {
                alert('Got an error');
            }
        });
    }
// , 2000)
