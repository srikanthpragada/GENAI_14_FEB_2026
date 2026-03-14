import sqlite3
import os

DB_PATH = r'c:\classroom\courses.db'


def connect_db():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: The database connection object.

    Raises:
        sqlite3.Error: If there is an error connecting to the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error connecting to database: {e}")


def create_course(title, duration, fee):
    """
    Creates a new course in the COURSES table.

    Args:
        title (str): The title of the course. Must be a non-empty string.
        duration (int): The duration of the course in hours. Must be a positive integer.
        fee (float): The fee for the course. Must be a non-negative float.

    Returns:
        int: The ID of the newly created course.

    Raises:
        ValueError: If any of the input validations fail.
        sqlite3.Error: If there is a database error during insertion.
    """
    # Validations
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must be a non-empty string.")
    title = title.strip()

    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("Duration must be a positive integer.")

    if not isinstance(fee, (int, float)) or fee < 0:
        raise ValueError("Fee must be a non-negative number.")

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO COURSES (title, duration, fee)
            VALUES (?, ?, ?)
        ''', (title, duration, fee))
        conn.commit()
        course_id = cursor.lastrowid
        return course_id
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise sqlite3.Error(f"Error creating course: {e}")
    finally:
        if conn:
            conn.close()


def get_all_courses():
    """
    Retrieves all courses from the COURSES table.

    Returns:
        list: A list of dictionaries, each representing a course with keys 'id', 'title', 'duration', 'fee'.

    Raises:
        sqlite3.Error: If there is a database error during retrieval.
    """
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, duration, fee FROM COURSES')
        rows = cursor.fetchall()
        courses = [{'id': row[0], 'title': row[1],
                    'duration': row[2], 'fee': row[3]} for row in rows]
        return courses
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error retrieving courses: {e}")
    finally:
        if conn:
            conn.close()


def get_course_by_id(course_id):
    """
    Retrieves a single course by its ID from the COURSES table.

    Args:
        course_id (int): The ID of the course to retrieve. Must be a positive integer.

    Returns:
        dict or None: A dictionary with keys 'id', 'title', 'duration', 'fee' if found, else None.

    Raises:
        ValueError: If course_id is not a positive integer.
        sqlite3.Error: If there is a database error during retrieval.
    """
    if not isinstance(course_id, int) or course_id <= 0:
        raise ValueError("Course ID must be a positive integer.")

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, title, duration, fee FROM COURSES WHERE id = ?', (course_id,))
        row = cursor.fetchone()
        if row:
            course = {'id': row[0], 'title': row[1],
                      'duration': row[2], 'fee': row[3]}
            return course
        else:
            return None
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error retrieving course: {e}")
    finally:
        if conn:
            conn.close()


def update_course(course_id, title=None, duration=None, fee=None):
    """
    Updates an existing course in the COURSES table. Only provided fields will be updated.

    Args:
        course_id (int): The ID of the course to update. Must be a positive integer.
        title (str, optional): The new title. Must be a non-empty string if provided.
        duration (int, optional): The new duration. Must be a positive integer if provided.
        fee (float, optional): The new fee. Must be a non-negative number if provided.

    Returns:
        bool: True if the update was successful, False if the course was not found.

    Raises:
        ValueError: If any input validations fail.
        sqlite3.Error: If there is a database error during update.
    """
    if not isinstance(course_id, int) or course_id <= 0:
        raise ValueError("Course ID must be a positive integer.")

    # Validations for provided fields
    if title is not None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string.")
        title = title.strip()

    if duration is not None:
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer.")

    if fee is not None:
        if not isinstance(fee, (int, float)) or fee < 0:
            raise ValueError("Fee must be a non-negative number.")

    # Check if at least one field is provided
    if all(param is None for param in [title, duration, fee]):
        raise ValueError(
            "At least one field (title, duration, or fee) must be provided for update.")

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Build the update query dynamically
        update_fields = []
        values = []
        if title is not None:
            update_fields.append('title = ?')
            values.append(title)
        if duration is not None:
            update_fields.append('duration = ?')
            values.append(duration)
        if fee is not None:
            update_fields.append('fee = ?')
            values.append(fee)

        values.append(course_id)
        query = f'UPDATE COURSES SET {", ".join(update_fields)} WHERE id = ?'

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False  # No rows updated, course not found
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise sqlite3.Error(f"Error updating course: {e}")
    finally:
        if conn:
            conn.close()


def delete_course(course_id):
    """
    Deletes a course from the COURSES table by its ID.

    Args:
        course_id (int): The ID of the course to delete. Must be a positive integer.

    Returns:
        bool: True if the deletion was successful, False if the course was not found.

    Raises:
        ValueError: If course_id is not a positive integer.
        sqlite3.Error: If there is a database error during deletion.
    """
    if not isinstance(course_id, int) or course_id <= 0:
        raise ValueError("Course ID must be a positive integer.")

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM COURSES WHERE id = ?', (course_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False  # No rows deleted, course not found
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise sqlite3.Error(f"Error deleting course: {e}")
    finally:
        if conn:
            conn.close()
