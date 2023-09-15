$(document).ready(function() {
    $('#validateBtn').click(function() {
        var selectedSignature = $('#signatureSelect').val();

        // Get the image data from the selectedSignature element
        var imageData = $('#selectedSignature').attr('src');

        // Send the image data to the backend for validation
        $.ajax({
            type: 'POST',
            url: '/validate_signature',
            data: {
                'selected_signature': selectedSignature,
                'image_data': imageData
            },
            success: function(data) {
                var validationResult = data.result;
                // Show the validation result in a popup
                alert('Validation Result: ' + validationResult);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#userSelect').change(function() {
        var selectedUser = $(this).val();

        $.ajax({
            type: 'POST',
            url: '/user_signatures',
            data: {'user_name': selectedUser},
            success: function(data) {
                var signatures = data.signatures;
                var genuineSignature = data.genuine_signature;
                var signatureSelect = $('#signatureSelect');

                signatureSelect.empty();
                $.each(signatures, function(index, signature) {
                    var parts = signature.split('/');
                    var fileName = parts[1];
                    // Remove the file extension
                    var fileNameWithoutExtension = fileName.split('.')[0];
                    signatureSelect.append($('<option>', {
                        value: signature,
                        text: fileNameWithoutExtension
                    }));
                });

                $('#genuineSignature').attr('src', '/static/images/img_list/' + genuineSignature);
                // Trigger the change event after populating the dropdown
                $('#signatureSelect').trigger('change');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#signatureSelect').change(function() {
        var selectedSignature = $(this).val();
        console.log(selectedSignature)
        $('#selectedSignature').attr('src', '/static/images/img_list/' + selectedSignature);
    });

    // Trigger the change event when the page loads
    $('#userSelect').trigger('change');
});
