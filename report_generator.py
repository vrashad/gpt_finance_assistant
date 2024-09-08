from config import OUTPUT_FILE_PATH


def generate_report(log, summary_list):
    log.info('Generating report')

    md_content = "# Stock Analysis Report\n\n"

    for summary in summary_list:
        md_content += f"## {summary['ticker']}\n\n"
        md_content += f"**Current Price:** ${summary['current_price']}\n\n"
        md_content += f"**Mention Count:** {summary['mention_count']}\n\n"
        md_content += f"**Summary:**\n{summary['gpt_summary']}\n\n"
        md_content += "---\n\n"

    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(md_content)

    log.info(f"Report generated and saved to {OUTPUT_FILE_PATH}")