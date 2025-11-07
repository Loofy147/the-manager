import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Plus, 
  Edit, 
  Trash2, 
  DollarSign,
  TrendingUp,
  TrendingDown,
  Calendar,
  FileText,
  Download,
  Upload,
  Search,
  Filter,
  AlertCircle,
  CheckCircle,
  Clock,
  CreditCard,
  Receipt,
  PieChart,
  BarChart3,
  Target,
  Wallet,
  Building,
  User,
  Eye,
  Send,
  Archive,
  RefreshCw
} from 'lucide-react'

// Mock data for financial management
const mockBudgets = [
  {
    id: '1',
    project_id: '1',
    project_name: 'نظام التعرف على الصور',
    total_budget: 50000,
    allocated_budget: 45000,
    spent_budget: 37500,
    remaining_budget: 12500,
    budget_categories: [
      { category: 'الرواتب', allocated: 25000, spent: 20000 },
      { category: 'الأجهزة', allocated: 10000, spent: 8500 },
      { category: 'البرمجيات', allocated: 5000, spent: 4000 },
      { category: 'التدريب', allocated: 3000, spent: 2500 },
      { category: 'أخرى', allocated: 2000, spent: 2500 }
    ],
    status: 'active',
    created_date: '2024-01-15',
    last_updated: '2024-06-15'
  },
  {
    id: '2',
    project_id: '2',
    project_name: 'منصة التجارة الإلكترونية',
    total_budget: 75000,
    allocated_budget: 70000,
    spent_budget: 15000,
    remaining_budget: 60000,
    budget_categories: [
      { category: 'الرواتب', allocated: 40000, spent: 8000 },
      { category: 'الاستضافة', allocated: 15000, spent: 3000 },
      { category: 'التصميم', allocated: 10000, spent: 2000 },
      { category: 'التسويق', allocated: 5000, spent: 2000 }
    ],
    status: 'active',
    created_date: '2024-03-01',
    last_updated: '2024-06-10'
  }
]

const mockExpenses = [
  {
    id: '1',
    project_id: '1',
    project_name: 'نظام التعرف على الصور',
    description: 'راتب مطور الذكاء الاصطناعي - يونيو',
    amount: 5000,
    category: 'الرواتب',
    type: 'recurring',
    status: 'approved',
    date: '2024-06-01',
    approved_by: 'أحمد محمد',
    receipt_url: '/receipts/receipt_001.pdf'
  },
  {
    id: '2',
    project_id: '1',
    project_name: 'نظام التعرف على الصور',
    description: 'خادم GPU للتدريب',
    amount: 2500,
    category: 'الأجهزة',
    type: 'one_time',
    status: 'pending',
    date: '2024-06-15',
    submitted_by: 'فاطمة علي'
  },
  {
    id: '3',
    project_id: '2',
    project_name: 'منصة التجارة الإلكترونية',
    description: 'ترخيص Adobe Creative Suite',
    amount: 600,
    category: 'البرمجيات',
    type: 'recurring',
    status: 'approved',
    date: '2024-06-10',
    approved_by: 'محمد حسن'
  }
]

const mockContracts = [
  {
    id: '1',
    title: 'عقد تطوير نظام التعرف على الصور',
    client: 'شركة التقنيات المتقدمة',
    project_id: '1',
    contract_type: 'development',
    value: 50000,
    currency: 'USD',
    status: 'active',
    start_date: '2024-01-15',
    end_date: '2024-06-30',
    payment_terms: 'شهري',
    milestones: [
      { name: 'جمع البيانات', amount: 12500, status: 'completed', due_date: '2024-02-15' },
      { name: 'تدريب النموذج', amount: 25000, status: 'in_progress', due_date: '2024-04-30' },
      { name: 'اختبار النشر', amount: 12500, status: 'pending', due_date: '2024-06-30' }
    ],
    terms_conditions: 'العقد يشمل تطوير نموذج ذكاء اصطناعي للتعرف على الصور مع ضمان دقة 95%',
    signed_date: '2024-01-10',
    contract_manager: 'أحمد محمد'
  },
  {
    id: '2',
    title: 'عقد تطوير منصة التجارة الإلكترونية',
    client: 'متجر الإلكترونيات الذكية',
    project_id: '2',
    contract_type: 'development',
    value: 75000,
    currency: 'USD',
    status: 'active',
    start_date: '2024-03-01',
    end_date: '2024-09-30',
    payment_terms: 'حسب المعالم',
    milestones: [
      { name: 'تصميم الواجهات', amount: 15000, status: 'completed', due_date: '2024-03-31' },
      { name: 'تطوير الخلفية', amount: 30000, status: 'in_progress', due_date: '2024-06-30' },
      { name: 'اختبار النظام', amount: 20000, status: 'pending', due_date: '2024-08-31' },
      { name: 'النشر والتدريب', amount: 10000, status: 'pending', due_date: '2024-09-30' }
    ],
    terms_conditions: 'تطوير منصة تجارة إلكترونية متكاملة مع نظام إدارة المخزون',
    signed_date: '2024-02-25',
    contract_manager: 'فاطمة علي'
  }
]

const mockInvoices = [
  {
    id: '1',
    invoice_number: 'INV-2024-001',
    contract_id: '1',
    client: 'شركة التقنيات المتقدمة',
    amount: 12500,
    status: 'paid',
    issue_date: '2024-02-15',
    due_date: '2024-03-15',
    paid_date: '2024-03-10',
    description: 'الدفعة الأولى - جمع البيانات',
    payment_method: 'تحويل بنكي'
  },
  {
    id: '2',
    invoice_number: 'INV-2024-002',
    contract_id: '1',
    client: 'شركة التقنيات المتقدمة',
    amount: 12500,
    status: 'pending',
    issue_date: '2024-04-30',
    due_date: '2024-05-30',
    description: 'الدفعة الثانية - تدريب النموذج (جزئي)',
    payment_method: 'تحويل بنكي'
  },
  {
    id: '3',
    invoice_number: 'INV-2024-003',
    contract_id: '2',
    client: 'متجر الإلكترونيات الذكية',
    amount: 15000,
    status: 'paid',
    issue_date: '2024-03-31',
    due_date: '2024-04-30',
    paid_date: '2024-04-25',
    description: 'تصميم الواجهات',
    payment_method: 'شيك'
  }
]

const expenseCategories = [
  'الرواتب', 'الأجهزة', 'البرمجيات', 'الاستضافة', 'التدريب', 
  'التسويق', 'السفر', 'المكتب', 'الاستشارات', 'أخرى'
]

const contractTypes = [
  { id: 'development', name: 'تطوير' },
  { id: 'consulting', name: 'استشارات' },
  { id: 'maintenance', name: 'صيانة' },
  { id: 'support', name: 'دعم فني' },
  { id: 'training', name: 'تدريب' }
]

function BudgetCard({ budget, onEdit, onViewDetails }) {
  const utilizationPercentage = (budget.spent_budget / budget.allocated_budget) * 100
  const isOverBudget = budget.spent_budget > budget.allocated_budget
  
  return (
    <Card className={`hover:shadow-lg transition-all duration-200 ${isOverBudget ? 'border-red-200' : ''}`}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg">{budget.project_name}</CardTitle>
            <CardDescription>
              آخر تحديث: {new Date(budget.last_updated).toLocaleDateString('ar')}
            </CardDescription>
          </div>
          <Badge variant={budget.status === 'active' ? 'default' : 'secondary'}>
            {budget.status === 'active' ? 'نشط' : 'مكتمل'}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Budget Overview */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">الميزانية الإجمالية:</span>
            <div className="font-bold text-lg">${budget.total_budget.toLocaleString()}</div>
          </div>
          <div>
            <span className="text-muted-foreground">المصروف:</span>
            <div className={`font-bold text-lg ${isOverBudget ? 'text-red-600' : 'text-green-600'}`}>
              ${budget.spent_budget.toLocaleString()}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm mb-2">
            <span>الاستخدام</span>
            <span className={isOverBudget ? 'text-red-600' : 'text-green-600'}>
              {utilizationPercentage.toFixed(1)}%
            </span>
          </div>
          <Progress 
            value={Math.min(utilizationPercentage, 100)} 
            className={`h-3 ${isOverBudget ? '[&>div]:bg-red-500' : ''}`}
          />
          {isOverBudget && (
            <div className="flex items-center gap-1 text-red-600 text-xs mt-1">
              <AlertCircle className="h-3 w-3" />
              تجاوز الميزانية بـ ${(budget.spent_budget - budget.allocated_budget).toLocaleString()}
            </div>
          )}
        </div>

        {/* Remaining Budget */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <span className="text-sm text-muted-foreground">المتبقي:</span>
          <span className={`font-bold ${budget.remaining_budget >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${Math.abs(budget.remaining_budget).toLocaleString()}
          </span>
        </div>

        {/* Top Categories */}
        <div className="space-y-2">
          <h5 className="text-sm font-medium">أعلى الفئات استهلاكاً:</h5>
          {budget.budget_categories
            .sort((a, b) => b.spent - a.spent)
            .slice(0, 3)
            .map((category, index) => (
              <div key={index} className="flex items-center justify-between text-xs">
                <span>{category.category}</span>
                <span className="font-medium">${category.spent.toLocaleString()}</span>
              </div>
            ))}
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          <Button variant="outline" size="sm" onClick={() => onViewDetails(budget)}>
            <Eye className="h-4 w-4 ml-1" />
            عرض التفاصيل
          </Button>
          <Button variant="outline" size="sm" onClick={() => onEdit(budget)}>
            <Edit className="h-4 w-4 ml-1" />
            تعديل
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

function ExpenseCard({ expense, onApprove, onReject, onEdit }) {
  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800'
  }

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h4 className="font-medium">{expense.description}</h4>
            <p className="text-sm text-muted-foreground">{expense.project_name}</p>
            <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
              <span>{new Date(expense.date).toLocaleDateString('ar')}</span>
              <Badge variant="outline">{expense.category}</Badge>
              <Badge variant="outline">
                {expense.type === 'recurring' ? 'متكرر' : 'مرة واحدة'}
              </Badge>
            </div>
          </div>
          
          <div className="text-left">
            <div className="text-lg font-bold">${expense.amount.toLocaleString()}</div>
            <Badge className={statusColors[expense.status]}>
              {expense.status === 'pending' ? 'معلق' :
               expense.status === 'approved' ? 'موافق عليه' : 'مرفوض'}
            </Badge>
          </div>
        </div>

        {expense.status === 'pending' && (
          <div className="flex gap-2 mt-4">
            <Button size="sm" onClick={() => onApprove(expense)}>
              <CheckCircle className="h-4 w-4 ml-1" />
              موافقة
            </Button>
            <Button variant="outline" size="sm" onClick={() => onReject(expense)}>
              <AlertCircle className="h-4 w-4 ml-1" />
              رفض
            </Button>
          </div>
        )}

        {expense.status === 'approved' && expense.approved_by && (
          <div className="text-xs text-muted-foreground mt-2">
            وافق عليه: {expense.approved_by}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function ContractCard({ contract, onEdit, onViewDetails, onGenerateInvoice }) {
  const completedMilestones = contract.milestones.filter(m => m.status === 'completed').length
  const totalMilestones = contract.milestones.length
  const completionPercentage = (completedMilestones / totalMilestones) * 100

  const statusColors = {
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    cancelled: 'bg-red-100 text-red-800',
    pending: 'bg-yellow-100 text-yellow-800'
  }

  return (
    <Card className="hover:shadow-lg transition-all duration-200">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg">{contract.title}</CardTitle>
            <CardDescription>{contract.client}</CardDescription>
          </div>
          <Badge className={statusColors[contract.status]}>
            {contract.status === 'active' ? 'نشط' :
             contract.status === 'completed' ? 'مكتمل' :
             contract.status === 'cancelled' ? 'ملغي' : 'معلق'}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Contract Value */}
        <div className="flex items-center justify-between">
          <span className="text-muted-foreground">قيمة العقد:</span>
          <span className="text-2xl font-bold text-green-600">
            ${contract.value.toLocaleString()} {contract.currency}
          </span>
        </div>

        {/* Progress */}
        <div>
          <div className="flex justify-between text-sm mb-2">
            <span>التقدم</span>
            <span>{completionPercentage.toFixed(0)}%</span>
          </div>
          <Progress value={completionPercentage} className="h-2" />
          <div className="text-xs text-muted-foreground mt-1">
            {completedMilestones} من {totalMilestones} معالم مكتملة
          </div>
        </div>

        {/* Contract Details */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">تاريخ البداية:</span>
            <div>{new Date(contract.start_date).toLocaleDateString('ar')}</div>
          </div>
          <div>
            <span className="text-muted-foreground">تاريخ النهاية:</span>
            <div>{new Date(contract.end_date).toLocaleDateString('ar')}</div>
          </div>
          <div>
            <span className="text-muted-foreground">شروط الدفع:</span>
            <div>{contract.payment_terms}</div>
          </div>
          <div>
            <span className="text-muted-foreground">مدير العقد:</span>
            <div>{contract.contract_manager}</div>
          </div>
        </div>

        {/* Next Milestone */}
        {contract.milestones.find(m => m.status === 'in_progress' || m.status === 'pending') && (
          <div className="p-3 bg-blue-50 rounded-lg">
            <h5 className="text-sm font-medium mb-1">المعلم القادم:</h5>
            {(() => {
              const nextMilestone = contract.milestones.find(m => m.status === 'in_progress') || 
                                   contract.milestones.find(m => m.status === 'pending')
              return (
                <div className="flex items-center justify-between text-sm">
                  <span>{nextMilestone.name}</span>
                  <div className="text-left">
                    <div className="font-medium">${nextMilestone.amount.toLocaleString()}</div>
                    <div className="text-xs text-muted-foreground">
                      {new Date(nextMilestone.due_date).toLocaleDateString('ar')}
                    </div>
                  </div>
                </div>
              )
            })()}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          <Button variant="outline" size="sm" onClick={() => onViewDetails(contract)}>
            <Eye className="h-4 w-4 ml-1" />
            عرض
          </Button>
          <Button variant="outline" size="sm" onClick={() => onEdit(contract)}>
            <Edit className="h-4 w-4 ml-1" />
            تعديل
          </Button>
          <Button variant="outline" size="sm" onClick={() => onGenerateInvoice(contract)}>
            <Receipt className="h-4 w-4 ml-1" />
            فاتورة
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

function CreateExpenseDialog({ open, onOpenChange }) {
  const [formData, setFormData] = useState({
    project_id: '',
    description: '',
    amount: 0,
    category: '',
    type: 'one_time',
    date: new Date().toISOString().split('T')[0],
    receipt_file: null
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Creating expense:', formData)
    onOpenChange(false)
    // Here you would call the API to create the expense
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>إضافة مصروف جديد</DialogTitle>
          <DialogDescription>
            إضافة مصروف جديد للمشروع
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="project_id">المشروع</Label>
            <Select value={formData.project_id} onValueChange={(value) => setFormData(prev => ({ ...prev, project_id: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="اختر المشروع" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">نظام التعرف على الصور</SelectItem>
                <SelectItem value="2">منصة التجارة الإلكترونية</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="description">الوصف</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              placeholder="وصف المصروف"
              required
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="amount">المبلغ ($)</Label>
              <Input
                id="amount"
                type="number"
                value={formData.amount}
                onChange={(e) => setFormData(prev => ({ ...prev, amount: parseFloat(e.target.value) }))}
                placeholder="0.00"
                step="0.01"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="date">التاريخ</Label>
              <Input
                id="date"
                type="date"
                value={formData.date}
                onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
                required
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="category">الفئة</Label>
            <Select value={formData.category} onValueChange={(value) => setFormData(prev => ({ ...prev, category: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="اختر الفئة" />
              </SelectTrigger>
              <SelectContent>
                {expenseCategories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="type">النوع</Label>
            <Select value={formData.type} onValueChange={(value) => setFormData(prev => ({ ...prev, type: value }))}>
              <SelectTrigger>
                <SelectValue placeholder="اختر النوع" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="one_time">مرة واحدة</SelectItem>
                <SelectItem value="recurring">متكرر</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="flex gap-2">
            <Button type="submit">إضافة المصروف</Button>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              إلغاء
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default function FinanceManagement() {
  const [activeTab, setActiveTab] = useState('budgets')
  const [budgets, setBudgets] = useState(mockBudgets)
  const [expenses, setExpenses] = useState(mockExpenses)
  const [contracts, setContracts] = useState(mockContracts)
  const [invoices, setInvoices] = useState(mockInvoices)
  const [createExpenseOpen, setCreateExpenseOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')

  const handleApproveExpense = (expense) => {
    console.log('Approving expense:', expense)
    // Here you would call the API to approve the expense
  }

  const handleRejectExpense = (expense) => {
    console.log('Rejecting expense:', expense)
    // Here you would call the API to reject the expense
  }

  const handleEditBudget = (budget) => {
    console.log('Editing budget:', budget)
    // Here you would open an edit dialog
  }

  const handleViewBudgetDetails = (budget) => {
    console.log('Viewing budget details:', budget)
    // Here you would open a details dialog
  }

  const handleEditContract = (contract) => {
    console.log('Editing contract:', contract)
    // Here you would open an edit dialog
  }

  const handleViewContractDetails = (contract) => {
    console.log('Viewing contract details:', contract)
    // Here you would open a details dialog
  }

  const handleGenerateInvoice = (contract) => {
    console.log('Generating invoice for contract:', contract)
    // Here you would generate an invoice
  }

  // Calculate summary statistics
  const totalBudget = budgets.reduce((sum, budget) => sum + budget.total_budget, 0)
  const totalSpent = budgets.reduce((sum, budget) => sum + budget.spent_budget, 0)
  const totalRemaining = budgets.reduce((sum, budget) => sum + budget.remaining_budget, 0)
  const pendingExpenses = expenses.filter(e => e.status === 'pending').length
  const activeContracts = contracts.filter(c => c.status === 'active').length
  const totalContractValue = contracts.reduce((sum, contract) => sum + contract.value, 0)

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">إدارة المالية والعقود</h2>
          <p className="text-muted-foreground">إدارة الميزانيات والمصروفات والعقود</p>
        </div>
        <Button onClick={() => setCreateExpenseOpen(true)}>
          <Plus className="h-4 w-4 ml-2" />
          مصروف جديد
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">إجمالي الميزانيات</p>
                <p className="text-2xl font-bold">${totalBudget.toLocaleString()}</p>
              </div>
              <Wallet className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">إجمالي المصروفات</p>
                <p className="text-2xl font-bold">${totalSpent.toLocaleString()}</p>
                <p className="text-xs text-muted-foreground">
                  {((totalSpent / totalBudget) * 100).toFixed(1)}% من الميزانية
                </p>
              </div>
              <TrendingDown className="h-8 w-8 text-red-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">المبلغ المتبقي</p>
                <p className="text-2xl font-bold text-green-600">${totalRemaining.toLocaleString()}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">العقود النشطة</p>
                <p className="text-2xl font-bold">{activeContracts}</p>
                <p className="text-xs text-muted-foreground">
                  ${totalContractValue.toLocaleString()} إجمالي القيمة
                </p>
              </div>
              <FileText className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="budgets">الميزانيات</TabsTrigger>
          <TabsTrigger value="expenses">المصروفات</TabsTrigger>
          <TabsTrigger value="contracts">العقود</TabsTrigger>
          <TabsTrigger value="invoices">الفواتير</TabsTrigger>
        </TabsList>
        
        <TabsContent value="budgets" className="space-y-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="البحث في الميزانيات..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {budgets.map((budget) => (
              <BudgetCard
                key={budget.id}
                budget={budget}
                onEdit={handleEditBudget}
                onViewDetails={handleViewBudgetDetails}
              />
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="expenses" className="space-y-6">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="البحث في المصروفات..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
            {pendingExpenses > 0 && (
              <Badge variant="destructive">
                {pendingExpenses} مصروف معلق
              </Badge>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {expenses.map((expense) => (
              <ExpenseCard
                key={expense.id}
                expense={expense}
                onApprove={handleApproveExpense}
                onReject={handleRejectExpense}
                onEdit={() => {}}
              />
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="contracts" className="space-y-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="البحث في العقود..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {contracts.map((contract) => (
              <ContractCard
                key={contract.id}
                contract={contract}
                onEdit={handleEditContract}
                onViewDetails={handleViewContractDetails}
                onGenerateInvoice={handleGenerateInvoice}
              />
            ))}
          </div>
        </TabsContent>
        
        <TabsContent value="invoices" className="space-y-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="البحث في الفواتير..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
          </div>

          <div className="space-y-4">
            {invoices.map((invoice) => (
              <Card key={invoice.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-4">
                        <div>
                          <h4 className="font-medium">{invoice.invoice_number}</h4>
                          <p className="text-sm text-muted-foreground">{invoice.client}</p>
                        </div>
                        <Badge variant={
                          invoice.status === 'paid' ? 'secondary' :
                          invoice.status === 'pending' ? 'default' : 'destructive'
                        }>
                          {invoice.status === 'paid' ? 'مدفوعة' :
                           invoice.status === 'pending' ? 'معلقة' : 'متأخرة'}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">{invoice.description}</p>
                      <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                        <span>تاريخ الإصدار: {new Date(invoice.issue_date).toLocaleDateString('ar')}</span>
                        <span>تاريخ الاستحقاق: {new Date(invoice.due_date).toLocaleDateString('ar')}</span>
                        {invoice.paid_date && (
                          <span>تاريخ الدفع: {new Date(invoice.paid_date).toLocaleDateString('ar')}</span>
                        )}
                      </div>
                    </div>
                    
                    <div className="text-left">
                      <div className="text-xl font-bold">${invoice.amount.toLocaleString()}</div>
                      {invoice.payment_method && (
                        <div className="text-xs text-muted-foreground">{invoice.payment_method}</div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      <CreateExpenseDialog
        open={createExpenseOpen}
        onOpenChange={setCreateExpenseOpen}
      />
    </div>
  )
}

