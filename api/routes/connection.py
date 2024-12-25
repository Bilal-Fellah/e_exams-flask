import os
from supabase import create_client, Client

url: str = os.environ.get("https://jqfljolmdgdpisbmmmgn.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpxZmxqb2xtZGdkcGlzYm1tbWduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUxNDIwMDYsImV4cCI6MjA1MDcxODAwNn0.B9L-ou-5OFxnN8kMiO0Cu1gyKYpx6rPipE5mDrimZW4")
supabase: Client = create_client(url, key)
