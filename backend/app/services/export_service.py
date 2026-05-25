from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import json


class ExportService:
    """Service for exporting meetings"""
    
    @staticmethod
    def to_markdown(meeting) -> str:
        """Export meeting to markdown format"""
        md = f"""# {meeting.title}

**Date:** {meeting.created_at.strftime('%Y-%m-%d %H:%M')}  
**Status:** {meeting.status}  
**Duration:** {meeting.audio_duration_seconds:.1f} seconds  

## Summary

{meeting.summary or 'No summary available'}

## Transcript

{meeting.transcript or 'No transcript available'}

## Action Items

"""
        
        if meeting.action_items:
            try:
                items = json.loads(meeting.action_items)
                for item in items:
                    md += f"- [ ] {item.get('task', '')} "
                    if item.get('owner'):
                        md += f"(Owner: {item['owner']})"
                    md += "\n"
            except:
                md += meeting.action_items + "\n"
        else:
            md += "No action items"
        
        md += "\n## Topics\n\n"
        if meeting.topics:
            try:
                topics = json.loads(meeting.topics)
                for topic in topics:
                    md += f"- {topic}\n"
            except:
                md += meeting.topics
        else:
            md += "No topics"
        
        return md
    
    @staticmethod
    def to_pdf(meeting) -> bytes:
        """Export meeting to PDF format"""
        from io import BytesIO
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#0066cc',
            spaceAfter=12,
        )
        story.append(Paragraph(meeting.title, title_style))
        
        # Metadata
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=10,
            textColor='#666666',
            spaceAfter=12,
        )
        meta = f"<b>Date:</b> {meeting.created_at.strftime('%Y-%m-%d %H:%M')}<br/>"
        meta += f"<b>Status:</b> {meeting.status}<br/>"
        meta += f"<b>Duration:</b> {meeting.audio_duration_seconds:.1f} seconds"
        story.append(Paragraph(meta, meta_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        if meeting.summary:
            story.append(Paragraph("Summary", styles['Heading2']))
            story.append(Paragraph(meeting.summary, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Transcript
        if meeting.transcript:
            story.append(Paragraph("Transcript", styles['Heading2']))
            story.append(Paragraph(meeting.transcript[:500] + "..." if len(meeting.transcript) > 500 else meeting.transcript, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Action Items
        if meeting.action_items:
            story.append(Paragraph("Action Items", styles['Heading2']))
            try:
                items = json.loads(meeting.action_items)
                for item in items:
                    text = f"• {item.get('task', '')}"
                    if item.get('owner'):
                        text += f" (Owner: {item['owner']})"
                    story.append(Paragraph(text, styles['Normal']))
            except:
                story.append(Paragraph(meeting.action_items, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
