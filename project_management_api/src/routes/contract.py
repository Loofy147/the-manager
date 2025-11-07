from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.contract import Contract, Cost, Budget
from datetime import datetime
import json

contract_bp = Blueprint('contract', __name__)

# Contract endpoints

@contract_bp.route('/contracts', methods=['GET'])
def get_contracts():
    """Get all contracts with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    contract_type = request.args.get('contract_type')
    client_id = request.args.get('client_id')
    project_id = request.args.get('project_id')
    search = request.args.get('search', '')
    
    query = Contract.query
    
    if status:
        query = query.filter(Contract.status == status)
    
    if contract_type:
        query = query.filter(Contract.contract_type == contract_type)
    
    if client_id:
        query = query.filter(Contract.client_id == client_id)
    
    if project_id:
        query = query.filter(Contract.project_id == project_id)
    
    if search:
        query = query.filter(
            (Contract.title.contains(search)) |
            (Contract.contract_number.contains(search)) |
            (Contract.description.contains(search))
        )
    
    contracts = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'contracts': [contract.to_dict() for contract in contracts.items],
        'total': contracts.total,
        'pages': contracts.pages,
        'current_page': page,
        'per_page': per_page
    })

@contract_bp.route('/contracts', methods=['POST'])
def create_contract():
    """Create a new contract"""
    data = request.json
    
    # Generate contract number if not provided
    contract_number = data.get('contract_number')
    if not contract_number:
        # Generate a simple contract number based on timestamp
        contract_number = f"CNT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    contract = Contract(
        contract_number=contract_number,
        title=data['title'],
        description=data.get('description'),
        contract_type=data.get('contract_type'),
        client_id=data.get('client_id'),
        project_id=data.get('project_id'),
        total_value=data.get('total_value'),
        currency=data.get('currency', 'USD'),
        payment_terms=data.get('payment_terms'),
        start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'draft'),
        payment_schedule=json.dumps(data.get('payment_schedule', [])),
        milestones=json.dumps(data.get('milestones', [])),
        deliverables=json.dumps(data.get('deliverables', [])),
        terms_and_conditions=data.get('terms_and_conditions'),
        penalty_clauses=json.dumps(data.get('penalty_clauses', [])),
        bonus_clauses=json.dumps(data.get('bonus_clauses', [])),
        intellectual_property_terms=data.get('intellectual_property_terms'),
        confidentiality_terms=data.get('confidentiality_terms'),
        termination_conditions=data.get('termination_conditions'),
        renewal_options=json.dumps(data.get('renewal_options', {})),
        contract_file_url=data.get('contract_file_url'),
        created_by=data.get('created_by')
    )
    
    db.session.add(contract)
    db.session.commit()
    return jsonify(contract.to_dict()), 201

@contract_bp.route('/contracts/<contract_id>', methods=['GET'])
def get_contract(contract_id):
    """Get a specific contract by ID"""
    contract = Contract.query.get_or_404(contract_id)
    contract_data = contract.to_dict()
    
    # Include related costs
    costs = Cost.query.filter_by(contract_id=contract_id).all()
    contract_data['costs'] = [cost.to_dict() for cost in costs]
    
    # Calculate total costs
    total_costs = sum(float(cost.amount) for cost in costs if cost.status == 'approved')
    contract_data['total_costs'] = total_costs
    
    return jsonify(contract_data)

@contract_bp.route('/contracts/<contract_id>', methods=['PUT'])
def update_contract(contract_id):
    """Update a contract"""
    contract = Contract.query.get_or_404(contract_id)
    data = request.json
    
    contract.title = data.get('title', contract.title)
    contract.description = data.get('description', contract.description)
    contract.contract_type = data.get('contract_type', contract.contract_type)
    contract.client_id = data.get('client_id', contract.client_id)
    contract.project_id = data.get('project_id', contract.project_id)
    contract.total_value = data.get('total_value', contract.total_value)
    contract.currency = data.get('currency', contract.currency)
    contract.payment_terms = data.get('payment_terms', contract.payment_terms)
    contract.status = data.get('status', contract.status)
    contract.terms_and_conditions = data.get('terms_and_conditions', contract.terms_and_conditions)
    contract.intellectual_property_terms = data.get('intellectual_property_terms', contract.intellectual_property_terms)
    contract.confidentiality_terms = data.get('confidentiality_terms', contract.confidentiality_terms)
    contract.termination_conditions = data.get('termination_conditions', contract.termination_conditions)
    contract.contract_file_url = data.get('contract_file_url', contract.contract_file_url)
    contract.signed_by_client = data.get('signed_by_client', contract.signed_by_client)
    contract.signed_by_company = data.get('signed_by_company', contract.signed_by_company)
    
    if data.get('start_date'):
        contract.start_date = datetime.fromisoformat(data['start_date'])
    
    if data.get('end_date'):
        contract.end_date = datetime.fromisoformat(data['end_date'])
    
    if data.get('client_signature_date'):
        contract.client_signature_date = datetime.fromisoformat(data['client_signature_date'])
    
    if data.get('company_signature_date'):
        contract.company_signature_date = datetime.fromisoformat(data['company_signature_date'])
    
    if 'payment_schedule' in data:
        contract.payment_schedule = json.dumps(data['payment_schedule'])
    
    if 'milestones' in data:
        contract.milestones = json.dumps(data['milestones'])
    
    if 'deliverables' in data:
        contract.deliverables = json.dumps(data['deliverables'])
    
    if 'penalty_clauses' in data:
        contract.penalty_clauses = json.dumps(data['penalty_clauses'])
    
    if 'bonus_clauses' in data:
        contract.bonus_clauses = json.dumps(data['bonus_clauses'])
    
    if 'renewal_options' in data:
        contract.renewal_options = json.dumps(data['renewal_options'])
    
    if 'amendments' in data:
        contract.amendments = json.dumps(data['amendments'])
    
    contract.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(contract.to_dict())

@contract_bp.route('/contracts/<contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    """Delete a contract"""
    contract = Contract.query.get_or_404(contract_id)
    
    # Check if contract has associated costs
    costs = Cost.query.filter_by(contract_id=contract_id).count()
    if costs > 0:
        return jsonify({'error': 'Cannot delete contract with associated costs'}), 400
    
    db.session.delete(contract)
    db.session.commit()
    return '', 204

@contract_bp.route('/contracts/<contract_id>/sign', methods=['POST'])
def sign_contract(contract_id):
    """Sign a contract"""
    contract = Contract.query.get_or_404(contract_id)
    data = request.json
    
    signer = data.get('signer')  # 'client' or 'company'
    
    if signer == 'client':
        contract.signed_by_client = True
        contract.client_signature_date = datetime.utcnow()
    elif signer == 'company':
        contract.signed_by_company = True
        contract.company_signature_date = datetime.utcnow()
    else:
        return jsonify({'error': 'Invalid signer'}), 400
    
    # If both parties have signed, activate the contract
    if contract.signed_by_client and contract.signed_by_company:
        contract.status = 'active'
    
    contract.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(contract.to_dict())

# Cost endpoints

@contract_bp.route('/costs', methods=['GET'])
def get_costs():
    """Get all costs with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    project_id = request.args.get('project_id')
    contract_id = request.args.get('contract_id')
    category = request.args.get('category')
    status = request.args.get('status')
    billing_type = request.args.get('billing_type')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Cost.query
    
    if project_id:
        query = query.filter(Cost.project_id == project_id)
    
    if contract_id:
        query = query.filter(Cost.contract_id == contract_id)
    
    if category:
        query = query.filter(Cost.category == category)
    
    if status:
        query = query.filter(Cost.status == status)
    
    if billing_type:
        query = query.filter(Cost.billing_type == billing_type)
    
    if date_from:
        query = query.filter(Cost.date_incurred >= datetime.fromisoformat(date_from))
    
    if date_to:
        query = query.filter(Cost.date_incurred <= datetime.fromisoformat(date_to))
    
    costs = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'costs': [cost.to_dict() for cost in costs.items],
        'total': costs.total,
        'pages': costs.pages,
        'current_page': page,
        'per_page': per_page
    })

@contract_bp.route('/costs', methods=['POST'])
def create_cost():
    """Create a new cost entry"""
    data = request.json
    
    cost = Cost(
        project_id=data.get('project_id'),
        contract_id=data.get('contract_id'),
        category=data.get('category'),
        subcategory=data.get('subcategory'),
        description=data['description'],
        amount=data['amount'],
        currency=data.get('currency', 'USD'),
        cost_type=data.get('cost_type'),
        billing_type=data.get('billing_type'),
        date_incurred=datetime.fromisoformat(data['date_incurred']) if data.get('date_incurred') else datetime.utcnow(),
        payment_date=datetime.fromisoformat(data['payment_date']) if data.get('payment_date') else None,
        vendor=data.get('vendor'),
        invoice_number=data.get('invoice_number'),
        receipt_url=data.get('receipt_url'),
        budget_allocation_id=data.get('budget_allocation_id'),
        tax_amount=data.get('tax_amount'),
        tax_rate=data.get('tax_rate'),
        notes=data.get('notes'),
        created_by=data.get('created_by')
    )
    
    db.session.add(cost)
    db.session.commit()
    return jsonify(cost.to_dict()), 201

@contract_bp.route('/costs/<cost_id>', methods=['GET'])
def get_cost(cost_id):
    """Get a specific cost by ID"""
    cost = Cost.query.get_or_404(cost_id)
    return jsonify(cost.to_dict())

@contract_bp.route('/costs/<cost_id>', methods=['PUT'])
def update_cost(cost_id):
    """Update a cost entry"""
    cost = Cost.query.get_or_404(cost_id)
    data = request.json
    
    cost.category = data.get('category', cost.category)
    cost.subcategory = data.get('subcategory', cost.subcategory)
    cost.description = data.get('description', cost.description)
    cost.amount = data.get('amount', cost.amount)
    cost.currency = data.get('currency', cost.currency)
    cost.cost_type = data.get('cost_type', cost.cost_type)
    cost.billing_type = data.get('billing_type', cost.billing_type)
    cost.vendor = data.get('vendor', cost.vendor)
    cost.invoice_number = data.get('invoice_number', cost.invoice_number)
    cost.receipt_url = data.get('receipt_url', cost.receipt_url)
    cost.status = data.get('status', cost.status)
    cost.budget_allocation_id = data.get('budget_allocation_id', cost.budget_allocation_id)
    cost.tax_amount = data.get('tax_amount', cost.tax_amount)
    cost.tax_rate = data.get('tax_rate', cost.tax_rate)
    cost.notes = data.get('notes', cost.notes)
    
    if data.get('date_incurred'):
        cost.date_incurred = datetime.fromisoformat(data['date_incurred'])
    
    if data.get('payment_date'):
        cost.payment_date = datetime.fromisoformat(data['payment_date'])
    
    cost.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(cost.to_dict())

@contract_bp.route('/costs/<cost_id>', methods=['DELETE'])
def delete_cost(cost_id):
    """Delete a cost entry"""
    cost = Cost.query.get_or_404(cost_id)
    db.session.delete(cost)
    db.session.commit()
    return '', 204

@contract_bp.route('/costs/<cost_id>/approve', methods=['POST'])
def approve_cost(cost_id):
    """Approve a cost entry"""
    cost = Cost.query.get_or_404(cost_id)
    data = request.json
    
    cost.status = 'approved'
    cost.approved_by = data.get('approved_by')
    cost.approval_date = datetime.utcnow()
    
    db.session.commit()
    return jsonify(cost.to_dict())

# Budget endpoints

@contract_bp.route('/budgets', methods=['GET'])
def get_budgets():
    """Get all budgets with optional filtering"""
    project_id = request.args.get('project_id')
    approval_status = request.args.get('approval_status')
    budget_period = request.args.get('budget_period')
    
    query = Budget.query
    
    if project_id:
        query = query.filter(Budget.project_id == project_id)
    
    if approval_status:
        query = query.filter(Budget.approval_status == approval_status)
    
    if budget_period:
        query = query.filter(Budget.budget_period == budget_period)
    
    budgets = query.all()
    return jsonify([budget.to_dict() for budget in budgets])

@contract_bp.route('/budgets', methods=['POST'])
def create_budget():
    """Create a new budget"""
    data = request.json
    
    budget = Budget(
        project_id=data.get('project_id'),
        name=data['name'],
        description=data.get('description'),
        total_budget=data['total_budget'],
        currency=data.get('currency', 'USD'),
        budget_period=data.get('budget_period'),
        start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        categories=json.dumps(data.get('categories', [])),
        approval_status=data.get('approval_status', 'pending'),
        notes=data.get('notes'),
        created_by=data.get('created_by')
    )
    
    # Calculate remaining budget
    budget.remaining_budget = budget.total_budget - budget.allocated_budget
    
    db.session.add(budget)
    db.session.commit()
    return jsonify(budget.to_dict()), 201

@contract_bp.route('/budgets/<budget_id>', methods=['GET'])
def get_budget(budget_id):
    """Get a specific budget by ID"""
    budget = Budget.query.get_or_404(budget_id)
    budget_data = budget.to_dict()
    
    # Include allocated costs
    costs = Cost.query.filter_by(budget_allocation_id=budget_id).all()
    budget_data['allocated_costs'] = [cost.to_dict() for cost in costs]
    
    # Calculate actual spent budget
    actual_spent = sum(float(cost.amount) for cost in costs if cost.status == 'approved')
    budget_data['actual_spent_budget'] = actual_spent
    budget_data['remaining_budget'] = float(budget.total_budget) - actual_spent
    
    return jsonify(budget_data)

@contract_bp.route('/budgets/<budget_id>', methods=['PUT'])
def update_budget(budget_id):
    """Update a budget"""
    budget = Budget.query.get_or_404(budget_id)
    data = request.json
    
    budget.name = data.get('name', budget.name)
    budget.description = data.get('description', budget.description)
    budget.total_budget = data.get('total_budget', budget.total_budget)
    budget.allocated_budget = data.get('allocated_budget', budget.allocated_budget)
    budget.spent_budget = data.get('spent_budget', budget.spent_budget)
    budget.currency = data.get('currency', budget.currency)
    budget.budget_period = data.get('budget_period', budget.budget_period)
    budget.approval_status = data.get('approval_status', budget.approval_status)
    budget.notes = data.get('notes', budget.notes)
    
    if data.get('start_date'):
        budget.start_date = datetime.fromisoformat(data['start_date'])
    
    if data.get('end_date'):
        budget.end_date = datetime.fromisoformat(data['end_date'])
    
    if 'categories' in data:
        budget.categories = json.dumps(data['categories'])
    
    if data.get('approved_by'):
        budget.approved_by = data['approved_by']
        budget.approval_date = datetime.utcnow()
    
    # Recalculate remaining budget
    budget.remaining_budget = budget.total_budget - budget.spent_budget
    
    # Increment revision number if significant changes
    if any(key in data for key in ['total_budget', 'categories', 'budget_period']):
        budget.revision_number += 1
    
    budget.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(budget.to_dict())

@contract_bp.route('/budgets/<budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    """Delete a budget"""
    budget = Budget.query.get_or_404(budget_id)
    
    # Check if budget has allocated costs
    costs = Cost.query.filter_by(budget_allocation_id=budget_id).count()
    if costs > 0:
        return jsonify({'error': 'Cannot delete budget with allocated costs'}), 400
    
    db.session.delete(budget)
    db.session.commit()
    return '', 204

@contract_bp.route('/budgets/<budget_id>/approve', methods=['POST'])
def approve_budget(budget_id):
    """Approve a budget"""
    budget = Budget.query.get_or_404(budget_id)
    data = request.json
    
    budget.approval_status = 'approved'
    budget.approved_by = data.get('approved_by')
    budget.approval_date = datetime.utcnow()
    
    db.session.commit()
    return jsonify(budget.to_dict())

# Financial reporting endpoints

@contract_bp.route('/financial-summary', methods=['GET'])
def get_financial_summary():
    """Get financial summary across projects and contracts"""
    project_id = request.args.get('project_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Base queries
    contract_query = Contract.query
    cost_query = Cost.query
    budget_query = Budget.query
    
    if project_id:
        contract_query = contract_query.filter(Contract.project_id == project_id)
        cost_query = cost_query.filter(Cost.project_id == project_id)
        budget_query = budget_query.filter(Budget.project_id == project_id)
    
    if date_from:
        cost_query = cost_query.filter(Cost.date_incurred >= datetime.fromisoformat(date_from))
    
    if date_to:
        cost_query = cost_query.filter(Cost.date_incurred <= datetime.fromisoformat(date_to))
    
    # Calculate totals
    contracts = contract_query.all()
    costs = cost_query.all()
    budgets = budget_query.all()
    
    total_contract_value = sum(float(c.total_value) for c in contracts if c.total_value)
    total_approved_costs = sum(float(c.amount) for c in costs if c.status == 'approved')
    total_pending_costs = sum(float(c.amount) for c in costs if c.status == 'pending')
    total_budget_allocated = sum(float(b.total_budget) for b in budgets if b.approval_status == 'approved')
    
    return jsonify({
        'total_contract_value': total_contract_value,
        'total_approved_costs': total_approved_costs,
        'total_pending_costs': total_pending_costs,
        'total_budget_allocated': total_budget_allocated,
        'budget_utilization': (total_approved_costs / total_budget_allocated * 100) if total_budget_allocated > 0 else 0,
        'contract_count': len(contracts),
        'cost_count': len(costs),
        'budget_count': len(budgets)
    })

