import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    Float,
    Enum,
    ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

# --- Enums ---

class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"

class JobStatus(str, PyEnum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# --- Models ---

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owned_orgs: Mapped[List["Org"]] = relationship("Org", back_populates="owner")
    uploaded_files: Mapped[List["File"]] = relationship("File", back_populates="uploader")

class Org(Base):
    __tablename__ = "orgs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="owned_orgs")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="org")

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orgs.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    org: Mapped["Org"] = relationship("Org", back_populates="projects")
    files: Mapped[List["File"]] = relationship("File", back_populates="project", cascade="all, delete-orphan")
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="project", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    s3_key: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    filetype: Mapped[str] = mapped_column(String, nullable=True) # e.g. "fastq", "vcf"
    size: Mapped[int] = mapped_column(Integer, default=0) # in bytes
    uploaded_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="files")
    uploader: Mapped["User"] = relationship("User", back_populates="uploaded_files")
    embeddings: Mapped[List["Embedding"]] = relationship("Embedding", back_populates="file", cascade="all, delete-orphan")

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) # e.g. "nextflow_pipeline_1"
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.PENDING)
    result_s3_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    logs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="jobs")

class Embedding(Base):
    """
    Stores vector embeddings for file content to be used in RAG.
    Note: For high-performance vector search in Postgres, enable 'pgvector' extension.
    For this MVP, we store as a standard float array or use the external Qdrant service.
    This table acts as a reference/cache.
    """
    __tablename__ = "embeddings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("files.id"), nullable=False)
    chunk_id: Mapped[int] = mapped_column(Integer, nullable=False) # Sequence number of the chunk
    vector: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=True) # The embedding vector
    text_snippet: Mapped[str] = mapped_column(Text, nullable=False) # The actual text content
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    file: Mapped["File"] = relationship("File", back_populates="embeddings")
