from datetime import datetime, timedelta
from sqlalchemy import create_engine
from typing import List
from db.models.models import CompanyMembership, Quiz, Question, UserAnswers, Notification
from logger import logger
from sqlalchemy.orm import sessionmaker


def create_postgres_connection():
    engine = create_engine("postgresql://postgres:postgres@postgres:5432/db")
    return engine


def get_all_company_members(connection):
    all_members = []
    try:
        Session = sessionmaker(bind=connection)
        session = Session()
        all_members = session.query(CompanyMembership).all()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        session.close()
    return all_members


def get_all_company_quizzes(connection, company_id: int) -> List[Quiz]:
    all_quizzes = []
    try:
        Session = sessionmaker(bind=connection)
        session = Session()
        all_quizzes = session.query(Quiz).filter_by(company_id=company_id).all()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        session.close()
    return all_quizzes

def get_all_questions(connection, quiz_id):
    all_questions = []
    try:
        Session = sessionmaker(bind=connection)
        session = Session()
        all_questions = session.query(Question).filter_by(quiz_id=quiz_id).all()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        session.close()
    return all_questions


def get_all_user_answers(connection, user_id, quiz_id):
    all_user_answers = []
    try:
        Session = sessionmaker(bind=connection)
        session = Session()
        all_user_answers = session.query(UserAnswers).filter_by(user_id=user_id, quiz_id=quiz_id).all()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        session.close()
    return all_user_answers


def create_notification(connection, user_id, notification_text):
    try:
        Session = sessionmaker(bind=connection)
        session = Session()
        notification = Notification(user_id=user_id, timestamp=datetime.utcnow(), status=True, text=notification_text)
        session.add(notification)
        session.commit()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def create_notifications():
    current_date = datetime.now()
    connection = create_postgres_connection()
    all_users = get_all_company_members(connection)

    for user in all_users:
        user_id = user.user_id
        company_id = user.company_id

        quizzes = get_all_company_quizzes(connection, company_id)

        for quiz in quizzes:
            quiz_id = quiz.quiz_id
            frequency = quiz.frequency_in_days

            questions = get_all_questions(connection, quiz_id)
            check_user_answers = get_all_user_answers(connection, user_id, quiz_id)

            if not check_user_answers:
                notification_text = f"Quiz {quiz.name} is available! Take the test right now!"
                create_notification(connection, user_id, notification_text)

            if len(check_user_answers) < len(questions):
                notification_text = f"Complete the quiz {quiz.name}"
                create_notification(connection, user_id, notification_text)

            if len(check_user_answers) == len(questions):
                last_user_answer = None
                max_timestamp = None

                for answer in check_user_answers:
                    if max_timestamp is None or answer.timestamp > max_timestamp:
                        max_timestamp = answer.timestamp
                        last_user_answer = answer

                if last_user_answer is not None and current_date - last_user_answer.timestamp >= timedelta(
                        days=frequency):
                    notification_text = f"The frequency in days {frequency} has already passed. Take the {quiz.name} test now!"
                    create_notification(connection, user_id, notification_text)
                else:
                    continue
