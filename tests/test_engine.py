import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date
from models.schema import Base, SurveyResponse


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_save_single_response(test_engine):
    response = SurveyResponse(
        full_name="Juan Dela Cruz",
        age=30,
        gender="Male",
        email="juan@example.com",
        date_of_visit=date.today(),
        qid="q1",
        question="How was the food?",
        answer="Excellent"
    )

    with Session(test_engine) as session:
        session.add(response)
        session.commit()

        result = session.query(SurveyResponse).first()
        assert result.full_name == "Juan Dela Cruz"
        assert result.age == 30
        assert result.answer == "Excellent"


def test_multiple_responses(test_engine):
    responses = [
        SurveyResponse(
            full_name="User A",
            age=25,
            gender="Male",
            email="a@example.com",
            date_of_visit=date.today(),
            qid="q1",
            question="Service rating",
            answer="Good"
        ),
        SurveyResponse(
            full_name="User B",
            age=22,
            gender="Female",
            email="b@example.com",
            date_of_visit=date.today(),
            qid="q2",
            question="Would you return?",
            answer="Yes"
        )
    ]

    with Session(test_engine) as session:
        session.add_all(responses)
        session.commit()

        result = session.query(SurveyResponse).all()
        assert len(result) == 2
        assert result[0].qid == "q1"
        assert result[1].qid == "q2"
