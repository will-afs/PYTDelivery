import json

def get_pdf_id(db_cursor, file_uri:str)->int:
    """Fetch the id of the PDF instance in database 
    whose 'file_uri' value matches with the one provided as parameter 

    Parameters:
    db_cursor : the cursor pointing to the database
    file_uri (str) : the URI pointing to the PDF file used to identify the PDF instance in database

    Returns:
    int: the ID of the PDF instance in database whose 'file_uri' value matches with the one provided as parameter, if any.
    """
    pdf_id = db_cursor.execute(
        'SELECT p.id'
        ' FROM pdf p'
        ' WHERE p.file_uri = ?',
        (file_uri,)
    ).fetchone()
    if pdf_id is not None:
        pdf_id = pdf_id['id']
    return pdf_id

def get_pdf(db_cursor, pdf_id:int)->dict:
    """Fetch the fields of the PDF instance in database identified by the id provided as parameter

    Parameters:
    db_cursor : the cursor pointing to the database
    pdf_id (int) : the ID of the PDF instance in database 

    Returns:
    dict: the fields of the PDF instance in database identified by the id provided as parameter
    """
    pdf_row = db_cursor.execute(
        'SELECT p.id, file_uri, metadata, content'
        ' FROM pdf p'
        ' WHERE p.id = ?',
        (pdf_id,)
    ).fetchone()
    pdf=None
    if pdf_row is not None:
        pdf = {
                "id":pdf_row['id'], 
                "file_uri":pdf_row['file_uri'],
                "metadata":json.loads(pdf_row['metadata']),
                "content":pdf_row['content']
            }        
    return pdf

def create_pdf(db_cursor, file_uri)->int:
    """Assuming PDF does not already exist in database, 
    create a new PDF instance in database

    Parameters:
    db_cursor : the cursor pointing to the database
    file_uri (str) : the URI assumed to point to the PDF file

    Returns:
    int: the ID of the created PDF instance, if any
    """
    pdf_id = db_cursor.execute(
                        "INSERT INTO pdf (file_uri) VALUES (?)",
                        (file_uri,),
                    ).lastrowid               
    db_cursor.commit()
    return pdf_id

def fill_pdf(db_cursor, pdf_id:int, metadata:str, content:str):
    """Fill the PDF instance in database identified by pdf_id

    Parameters:
    db_cursor : the cursor pointing to the database
    pdf_id (int) : the ID of the PDF instance in database 
    file_uri (str) : the URI pointing to the PDF to use to fill PDF instance in database
    metadata (str) : the metadata of the PDF
    content (str) : the content of the PDF
    """            
    db_cursor.execute(
                        'UPDATE pdf SET metadata = ?, content = ?'
                        'WHERE id = ?',
                        (metadata, content, pdf_id),
                    )
    db_cursor.commit()