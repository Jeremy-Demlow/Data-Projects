from django import forms


class StorageForm(forms.Form):

    # Cloud storage
    cloud_options = list(zip(range(4), ["Azure Blob", "None"]))
    cloud_type = forms.ChoiceField(label='Persistent Cloud Storage',
                                   choices=cloud_options,
                                   widget=forms.RadioSelect,
                                   initial=cloud_options[0])

    # Table options
    table_options = list(zip(range(4), ["Create New Table", "Append to Existing Table", "Replace Existing Table"]))
    table_type = forms.ChoiceField(label='Table Insertion Options',
                                   choices=table_options,
                                   widget=forms.RadioSelect,
                                   initial=table_options[0])

    # Azure Stuff
    blob_account = forms.CharField(label='Azure Blob Storage Account', max_length=200)
    connection_str = forms.CharField(label='Azure Blob Connection String', max_length=200, widget=forms.PasswordInput)
    container = forms.CharField(label='Azure Blob Container', max_length=200)
    sas_token = forms.CharField(label='Azure Blob SAS Token', max_length=200, widget=forms.PasswordInput)

    # Snowflake Stuff
    sf_user = forms.CharField(label='Snowflake User', max_length=200)
    sf_password = forms.CharField(label='Snowflake Password', max_length=200, widget=forms.PasswordInput)
    sf_server = forms.CharField(label='Snowflake Server', max_length=200)
    sf_db = forms.CharField(label='Snowflake Database', max_length=200)
    sf_wh = forms.CharField(label='Snowflake Warehouse', max_length=200)
    sf_table = forms.CharField(label='Snowflake Table', max_length=200)
    sf_schema = forms.CharField(label='Snowflake Schema', max_length=200)
    sf_role = forms.CharField(label='Snowflake Role', max_length=200)

    # File Handling
    upsert_file = forms.FileField(label="Upsert File")


class InputCSVSnowflake(forms.Form):

    # Table options
    table_options = list(zip(range(4), ["Create New Table", "Append to Existing Table", "Replace Existing Table"]))
    table_type = forms.ChoiceField(label='Table Insertion Options',
                                   choices=table_options,
                                   widget=forms.RadioSelect,
                                   initial=table_options[0])

    # Snowflake Stuff
    sf_user = forms.CharField(label='Snowflake User', max_length=200)
    sf_password = forms.CharField(label='Snowflake Password', max_length=200, widget=forms.PasswordInput)
    sf_server = forms.CharField(label='Snowflake Server', max_length=200)
    sf_db = forms.CharField(label='Snowflake Database', max_length=200)
    sf_wh = forms.CharField(label='Snowflake Warehouse', max_length=200)
    sf_table = forms.CharField(label='Snowflake Table', max_length=200)
    sf_schema = forms.CharField(label='Snowflake Schema', max_length=200)
    sf_role = forms.CharField(label='Snowflake Role', max_length=200)

    # File Handling
    upsert_file = forms.FileField(label="Upsert File")


class InputCSVAzureSnowflake(forms.Form):

    # Table options
    table_options = list(zip(range(4), ["Create New Table", "Append to Existing Table", "Replace Existing Table"]))
    table_type = forms.ChoiceField(label='Table Insertion Options',
                                   choices=table_options,
                                   widget=forms.RadioSelect,
                                   initial=table_options[0])

    # Azure Stuff
    blob_account = forms.CharField(label='Azure Blob Storage Account', max_length=200)
    connection_str = forms.CharField(label='Azure Blob Connection String', max_length=200, widget=forms.PasswordInput)
    container = forms.CharField(label='Azure Blob Container', max_length=200)
    sas_token = forms.CharField(label='Azure Blob SAS Token', max_length=200, widget=forms.PasswordInput)

    # Snowflake Stuff
    sf_user = forms.CharField(label='Snowflake User', max_length=200)
    sf_password = forms.CharField(label='Snowflake Password', max_length=200, widget=forms.PasswordInput)
    sf_server = forms.CharField(label='Snowflake Server', max_length=200)
    sf_db = forms.CharField(label='Snowflake Database', max_length=200)
    sf_wh = forms.CharField(label='Snowflake Warehouse', max_length=200)
    sf_table = forms.CharField(label='Snowflake Table', max_length=200)
    sf_schema = forms.CharField(label='Snowflake Schema', max_length=200)
    sf_role = forms.CharField(label='Snowflake Role', max_length=200)

    # File Handling
    upsert_file = forms.FileField(label="Upsert File")