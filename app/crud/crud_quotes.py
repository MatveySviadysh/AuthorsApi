from fastcrud import FastCRUD

from db.models.author_orm_model import QuotesORM
from schemas.quotes import Quote, QuoteCreateInternal, QuoteUpdate, QuoteUpdateInternal, QuoteDelete

CRUDQuote= FastCRUD[Quote, QuoteCreateInternal, QuoteUpdate, QuoteUpdateInternal, QuoteDelete]
crud_quotes = CRUDQuote(QuotesORM)