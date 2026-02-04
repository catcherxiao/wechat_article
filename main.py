import json
import random
import sys
import os
import argparse
import datetime

# 定义颜色代码，提升 CLI 体验
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_operation(input_file, output_file, status="SUCCESS"):
    """记录操作日志"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Status: {status} | Input: {input_file} | Output: {output_file}\n"
    
    with open(os.path.join(log_dir, "operations.log"), "a", encoding="utf-8") as f:
        f.write(log_entry)

def load_quotes():
    """加载语录库"""
    try:
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        quotes_path = os.path.join(script_dir, 'quotes.json')
        
        with open(quotes_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colors.FAIL}错误: 找不到 quotes.json 文件。{Colors.ENDC}")
        sys.exit(1)

def find_relevant_quotes(user_text, quotes, limit=3):
    """简单的关键词匹配语录"""
    relevant = []
    user_text_lower = user_text.lower()
    
    # 关键词映射
    keywords = {
        "护城河": ["moat", "护城河"],
        "管理": ["management", "管理"],
        "价格": ["price", "valuation", "价格", "估值"],
        "价值": ["value", "价值"],
        "长期": ["time", "long", "时间", "长期"],
        "生意": ["business", "生意", "模式"],
        "错误": ["wrong", "mistake", "错"],
        "现金流": ["cash", "现金流"],
        "快乐": ["happy", "快乐", "悦己"],
        "收藏": ["collection", "收藏"],
        "迪士尼": ["disney", "迪士尼", "乐园"]
    }

    found_keys = []
    for key, tags in keywords.items():
        if key in user_text_lower:
            found_keys.extend(tags)

    # 查找匹配的语录
    for quote in quotes:
        for tag in quote.get('tags', []):
            if tag in found_keys:
                if quote not in relevant:
                    relevant.append(quote)

    # 如果没有匹配到，或者数量不足，随机补充
    if len(relevant) < limit:
        remaining = [q for q in quotes if q not in relevant]
        relevant.extend(random.sample(remaining, min(limit - len(relevant), len(remaining))))
    
    return relevant[:limit]

def generate_prompt(user_text, quotes):
    """生成最终的 System Prompt"""
    
    quotes_text = "\n".join([f"- {q['content_cn']} —— {q['author_cn']}" for q in quotes])
    
    prompt = f"""
# Role
你是一位拥有20年经验的顶级价值投资者，笔名“方伟”。你是巴菲特、芒格和段永平的忠实信徒。

# Style & Tone
你的写作风格冷静、克制、讲人话。你用商业常识、人性与场景把问题讲透，不堆术语，不装神秘。
1. **结构**：先一句话结论，再用 3-5 个小标题层层展开；每一段回答“为什么 / 所以什么 / 怎么验证”。
2. **思维模型**：
    - 区分“真护城河”（品牌、网络效应、转换成本）与“假护城河”（管理好、营销好、技术领先）。
    - 将生意分为：躺赚型（茅台）、稳赚型（腾讯/苹果）、辛苦钱（小米/拼多多）。
    - 极度关注长期（5-10年）的确定性，而非短期的股价波动。
3. **写法**：
    - 善用对比（A vs B）与类比（比如“水龙头 vs 喷泉”），把抽象词落到具体场景。
    - 适度使用反问句引导读者思考，但不过度煽情。
    - 有数据就用数据；没有数据就用可验证的观察与逻辑，不编数字、不编细节。
    - 句子偏短，段落之间多留白；关键句可以加粗。
4. **语言习惯**：
    - 喜欢引用巴菲特、芒格、段永平的语录来佐证观点。
    - 常用过渡句：如“简而言之”“换句话说”“反过来想”“我说一个假设”。
    - 语气平和但坚定，常使用反问句引发读者思考（例如：“这难道不是显而易见的数学题吗？”）。
    - 拒绝宏大叙事，回归生意赚多少钱、怎么赚钱的本质。

# Context (Reference Quotes)
在润色文章时，请适当自然地融入以下大师语录（如果相关）：
{quotes_text}

# Task
请将用户输入的文章/文字重写为一篇具有深度洞察力的投资笔记。
要求：
1. **保留原意**：保留原文关于“收藏变迁”、“悦己消费”、“微乐园”的核心观点。
2. **风格升华**：用“用户需求—消费场景—商业模式”的视角重写。例如，将“快乐”写成一种高频、低门槛、可复购的情绪价值。
3. **纠正误区**：如果原文有过于感性的描述，请用理性的商业逻辑重新包装。
4. **结构优化**：使用清晰的小标题，逻辑层层递进。
5. **输出格式**：Markdown 格式。

# User Input
{user_text}
"""
    return prompt

def main():
    parser = argparse.ArgumentParser(description="投资智慧回响 - Prompt 生成工具")
    parser.add_argument("-i", "--input", help="输入文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    quotes = load_quotes()

    # 文件处理模式
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                user_content = f.read()
            
            selected_quotes = find_relevant_quotes(user_content, quotes, limit=5)
            final_prompt = generate_prompt(user_content, selected_quotes)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(final_prompt)
                print(f"{Colors.GREEN}Prompt 已生成并保存至: {args.output}{Colors.ENDC}")
                log_operation(args.input, args.output, "SUCCESS")
            else:
                print(final_prompt)
                log_operation(args.input, "stdout", "SUCCESS")
                
        except Exception as e:
            print(f"{Colors.FAIL}处理文件时出错: {e}{Colors.ENDC}")
            log_operation(args.input, args.output if args.output else "stdout", f"FAILED: {str(e)}")
            sys.exit(1)
            
    # 交互模式
    else:
        print(f"{Colors.CYAN}{Colors.BOLD}欢迎使用【投资智慧回响】工具{Colors.ENDC}")
        print(f"{Colors.CYAN}这是一个帮助你像巴菲特和段永平一样思考的写作辅助器。{Colors.ENDC}\n")
        
        while True:
            try:
                user_input = input(f"{Colors.GREEN}请输入你想表达的想法或草稿 (输入 'q' 退出): {Colors.ENDC}")
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print("再见！愿时间是你的朋友。")
                    break
                
                if not user_input.strip():
                    continue
                    
                print(f"\n{Colors.BLUE}正在检索大师语录...{Colors.ENDC}")
                selected_quotes = find_relevant_quotes(user_input, quotes)
                
                print(f"\n{Colors.BLUE}正在构建风格化 Prompt...{Colors.ENDC}\n")
                final_prompt = generate_prompt(user_input, selected_quotes)
                
                print(final_prompt)
                print(f"\n{Colors.WARNING}提示：请复制上方两条横线之间的内容发送给 AI。{Colors.ENDC}\n")
                
                # 记录交互模式的日志
                log_operation("interactive_input", "interactive_output", "SUCCESS")
                
            except KeyboardInterrupt:
                print("\n再见！")
                break

if __name__ == "__main__":
    main()
