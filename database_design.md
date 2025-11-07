
# تصميم قاعدة البيانات والنماذج لنظام إدارة المشاريع

## مقدمة

يتطلب نظام إدارة المشاريع الشامل تصميم قاعدة بيانات قوية ومرنة تدعم التفرع الهرمي للأدوار، إدارة المشاريع والمهام، التكاليف والعقود، مع التركيز على مشاريع الذكاء الاصطناعي. سيتم تصميم النماذج بناءً على مبادئ Domain-Driven Design (DDD) لضمان الوضوح والقابلية للصيانة.

## 1. النماذج الأساسية (Core Models)

### 1.1 نموذج المستخدم (User Model)

نموذج المستخدم يمثل الأساس لجميع التفاعلات في النظام ويحتوي على المعلومات الشخصية والمهنية للمستخدمين.

```python
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    phone: str
    profile_image: str
    bio: str
    skills: List[str]
    experience_level: str  # junior, mid, senior, expert
    hourly_rate: Decimal
    availability_status: str  # available, busy, unavailable
    timezone: str
    language_preferences: List[str]
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    is_active: bool
    is_verified: bool
    verification_token: str
    reset_password_token: str
    reset_password_expires: datetime
```

### 1.2 نموذج الدور (Role Model)

نموذج الدور يدعم التفرع الهرمي ويسمح بإنشاء أدوار فرعية تحت أدوار رئيسية، مما يوفر مرونة في إدارة الصلاحيات والمسؤوليات.

```python
class Role:
    id: UUID
    name: str
    description: str
    parent_role_id: UUID  # للتفرع الهرمي
    level: int  # مستوى الدور في الهرم
    path: str  # مسار الدور في الهرم (مثل: /admin/project_manager/team_lead)
    permissions: List[str]
    max_subordinates: int  # الحد الأقصى للمرؤوسين
    can_create_subroles: bool
    can_assign_roles: bool
    can_manage_projects: bool
    can_manage_budgets: bool
    can_view_reports: bool
    salary_range_min: Decimal
    salary_range_max: Decimal
    required_skills: List[str]
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
```

### 1.3 نموذج تعيين الدور (UserRole Model)

هذا النموذج يربط المستخدمين بالأدوار ويدعم التعيينات المؤقتة والدائمة.

```python
class UserRole:
    id: UUID
    user_id: UUID
    role_id: UUID
    assigned_by: UUID
    assigned_at: datetime
    expires_at: datetime  # للتعيينات المؤقتة
    is_primary: bool  # الدور الأساسي للمستخدم
    status: str  # active, suspended, expired
    notes: str
    approval_status: str  # pending, approved, rejected
    approved_by: UUID
    approved_at: datetime
```

## 2. نماذج إدارة المشاريع

### 2.1 نموذج المشروع (Project Model)

نموذج المشروع يدعم أنواع مختلفة من المشاريع مع التركيز على مشاريع الذكاء الاصطناعي.

```python
class Project:
    id: UUID
    name: str
    description: str
    project_type: str  # ai_ml, web_development, mobile_app, data_analysis, etc.
    ai_project_category: str  # nlp, computer_vision, recommendation, prediction, etc.
    status: str  # planning, active, on_hold, completed, cancelled
    priority: str  # low, medium, high, critical
    start_date: datetime
    end_date: datetime
    estimated_duration: int  # في الأيام
    actual_duration: int
    budget: Decimal
    spent_budget: Decimal
    currency: str
    client_id: UUID
    project_manager_id: UUID
    team_lead_id: UUID
    repository_url: str
    documentation_url: str
    demo_url: str
    technologies: List[str]
    ai_frameworks: List[str]  # tensorflow, pytorch, scikit-learn, etc.
    datasets_used: List[str]
    model_performance_metrics: dict
    deployment_environment: str  # development, staging, production
    compliance_requirements: List[str]
    risk_assessment: str
    success_criteria: List[str]
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    is_archived: bool
```

### 2.2 نموذج المهمة (Task Model)

نموذج المهمة يدعم التفرع الهرمي للمهام ويسمح بإنشاء مهام فرعية.

```python
class Task:
    id: UUID
    title: str
    description: str
    project_id: UUID
    parent_task_id: UUID  # للمهام الفرعية
    assigned_to: UUID
    assigned_by: UUID
    status: str  # todo, in_progress, review, testing, completed, blocked
    priority: str  # low, medium, high, critical
    difficulty: str  # easy, medium, hard, expert
    estimated_hours: int
    actual_hours: int
    start_date: datetime
    due_date: datetime
    completed_at: datetime
    tags: List[str]
    dependencies: List[UUID]  # المهام التي تعتمد عليها
    attachments: List[str]
    comments: List[dict]
    progress_percentage: int
    quality_score: int  # 1-10
    code_review_status: str  # pending, approved, needs_changes
    testing_status: str  # not_tested, passed, failed
    ai_model_metrics: dict  # للمهام المتعلقة بالذكاء الاصطناعي
    created_by: UUID
    created_at: datetime
    updated_at: datetime
```

### 2.3 نموذج فريق المشروع (ProjectTeam Model)

```python
class ProjectTeam:
    id: UUID
    project_id: UUID
    user_id: UUID
    role_in_project: str  # project_manager, developer, designer, tester, etc.
    responsibilities: List[str]
    access_level: str  # read, write, admin
    joined_at: datetime
    left_at: datetime
    is_active: bool
    performance_rating: int  # 1-10
    contribution_percentage: int
    billable_rate: Decimal
```

## 3. نماذج إدارة التكاليف والعقود

### 3.1 نموذج العقد (Contract Model)

```python
class Contract:
    id: UUID
    contract_number: str
    title: str
    description: str
    contract_type: str  # fixed_price, hourly, milestone_based, retainer
    client_id: UUID
    project_id: UUID
    total_value: Decimal
    currency: str
    payment_terms: str
    start_date: datetime
    end_date: datetime
    status: str  # draft, active, completed, terminated, expired
    payment_schedule: List[dict]
    milestones: List[dict]
    deliverables: List[str]
    terms_and_conditions: str
    penalty_clauses: List[dict]
    bonus_clauses: List[dict]
    intellectual_property_terms: str
    confidentiality_terms: str
    termination_conditions: str
    renewal_options: dict
    signed_by_client: bool
    signed_by_company: bool
    client_signature_date: datetime
    company_signature_date: datetime
    contract_file_url: str
    amendments: List[dict]
    created_by: UUID
    created_at: datetime
    updated_at: datetime
```

### 3.2 نموذج التكلفة (Cost Model)

```python
class Cost:
    id: UUID
    project_id: UUID
    contract_id: UUID
    category: str  # labor, software, hardware, infrastructure, training, etc.
    subcategory: str
    description: str
    amount: Decimal
    currency: str
    cost_type: str  # fixed, variable, recurring
    billing_type: str  # billable, non_billable, internal
    date_incurred: datetime
    payment_date: datetime
    vendor: str
    invoice_number: str
    receipt_url: str
    approved_by: UUID
    approval_date: datetime
    status: str  # pending, approved, rejected, paid
    budget_allocation_id: UUID
    tax_amount: Decimal
    tax_rate: Decimal
    notes: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime
```

### 3.3 نموذج الميزانية (Budget Model)

```python
class Budget:
    id: UUID
    project_id: UUID
    name: str
    description: str
    total_budget: Decimal
    allocated_budget: Decimal
    spent_budget: Decimal
    remaining_budget: Decimal
    currency: str
    budget_period: str  # monthly, quarterly, yearly, project_lifetime
    start_date: datetime
    end_date: datetime
    categories: List[dict]  # تفصيل الميزانية حسب الفئات
    approval_status: str  # pending, approved, rejected
    approved_by: UUID
    approval_date: datetime
    revision_number: int
    notes: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime
```

## 4. نماذج الذكاء الاصطناعي المتخصصة

### 4.1 نموذج نموذج الذكاء الاصطناعي (AIModel Model)

```python
class AIModel:
    id: UUID
    name: str
    description: str
    project_id: UUID
    model_type: str  # classification, regression, clustering, nlp, computer_vision, etc.
    algorithm: str  # random_forest, neural_network, svm, etc.
    framework: str  # tensorflow, pytorch, scikit-learn, etc.
    version: str
    training_dataset_id: UUID
    validation_dataset_id: UUID
    test_dataset_id: UUID
    hyperparameters: dict
    performance_metrics: dict  # accuracy, precision, recall, f1_score, etc.
    training_duration: int  # في الدقائق
    model_size: int  # في الميجابايت
    inference_time: float  # في الميلي ثانية
    deployment_status: str  # development, staging, production, retired
    model_file_url: str
    documentation_url: str
    api_endpoint: str
    monitoring_metrics: dict
    bias_assessment: dict
    explainability_report: str
    compliance_status: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime
```

### 4.2 نموذج مجموعة البيانات (Dataset Model)

```python
class Dataset:
    id: UUID
    name: str
    description: str
    project_id: UUID
    dataset_type: str  # training, validation, test, production
    data_source: str  # internal, external, synthetic, web_scraping, etc.
    file_format: str  # csv, json, parquet, images, audio, video, etc.
    file_size: int  # في الميجابايت
    record_count: int
    feature_count: int
    target_variable: str
    data_quality_score: int  # 1-10
    missing_values_percentage: float
    duplicate_records_percentage: float
    data_schema: dict
    preprocessing_steps: List[str]
    data_lineage: List[dict]
    privacy_level: str  # public, internal, confidential, restricted
    retention_period: int  # في الأيام
    storage_location: str
    access_permissions: List[dict]
    last_updated: datetime
    version: str
    checksum: str
    created_by: UUID
    created_at: datetime
```

## 5. نماذج المراقبة والتقارير

### 5.1 نموذج التقرير (Report Model)

```python
class Report:
    id: UUID
    title: str
    description: str
    report_type: str  # project_status, financial, performance, ai_model_performance, etc.
    project_id: UUID
    generated_by: UUID
    generated_at: datetime
    report_period_start: datetime
    report_period_end: datetime
    data_sources: List[str]
    metrics: dict
    visualizations: List[dict]
    insights: List[str]
    recommendations: List[str]
    file_url: str
    sharing_permissions: List[dict]
    is_automated: bool
    schedule: str  # للتقارير المجدولة
    next_generation: datetime
    status: str  # generating, completed, failed
    created_at: datetime
```

### 5.2 نموذج المقاييس (Metrics Model)

```python
class Metrics:
    id: UUID
    project_id: UUID
    user_id: UUID
    metric_type: str  # productivity, quality, performance, cost, etc.
    metric_name: str
    metric_value: float
    unit: str
    measurement_date: datetime
    context: dict  # معلومات إضافية حول السياق
    benchmark_value: float
    target_value: float
    trend: str  # improving, declining, stable
    created_at: datetime
```

## 6. العلاقات بين النماذج

تتميز قاعدة البيانات بشبكة معقدة من العلاقات التي تربط بين النماذج المختلفة لضمان تكامل البيانات والحفاظ على الاتساق.

### 6.1 العلاقات الهرمية

العلاقات الهرمية تسمح بإنشاء هياكل متدرجة للأدوار والمهام والمشاريع، مما يوفر مرونة في التنظيم والإدارة.

**الأدوار الهرمية:** كل دور يمكن أن يحتوي على أدوار فرعية من خلال العلاقة `parent_role_id`. هذا يسمح بإنشاء هيكل تنظيمي معقد حيث يمكن للأدوار العليا إدارة الأدوار السفلى والتحكم في صلاحياتها.

**المهام الفرعية:** المهام يمكن أن تحتوي على مهام فرعية من خلال `parent_task_id`، مما يسمح بتقسيم المهام الكبيرة إلى مهام أصغر وأكثر قابلية للإدارة.

### 6.2 علاقات المشاريع

المشاريع تربط بين عدة نماذج مختلفة لتكوين نظام متكامل لإدارة دورة حياة المشروع الكاملة.

**فرق المشروع:** كل مشروع يحتوي على فريق من المستخدمين مع أدوار مختلفة من خلال نموذج `ProjectTeam`. هذا يسمح بتتبع مساهمات كل عضو في الفريق وإدارة الصلاحيات بشكل دقيق.

**المهام والمشاريع:** كل مهمة ترتبط بمشروع واحد، ولكن المشروع يمكن أن يحتوي على عدد غير محدود من المهام. هذا يسمح بتنظيم العمل وتتبع التقدم على مستوى المشروع والمهمة.

**التكاليف والميزانيات:** كل مشروع يحتوي على ميزانية وتكاليف مرتبطة به، مما يسمح بمراقبة الأداء المالي وضمان عدم تجاوز الميزانية المحددة.

### 6.3 علاقات الذكاء الاصطناعي

نماذج الذكاء الاصطناعي ترتبط بالمشاريع ومجموعات البيانات لتكوين نظام متكامل لإدارة مشاريع الذكاء الاصطناعي.

**النماذج ومجموعات البيانات:** كل نموذج ذكاء اصطناعي يرتبط بمجموعات بيانات متعددة للتدريب والتحقق والاختبار. هذا يسمح بتتبع أداء النموذج وضمان جودة البيانات المستخدمة.

**النماذج والمشاريع:** كل نموذج ذكاء اصطناعي ينتمي إلى مشروع واحد، ولكن المشروع يمكن أن يحتوي على عدة نماذج. هذا يسمح بإدارة متعددة النماذج في مشروع واحد وتتبع تطورها.

## 7. فهارس قاعدة البيانات

لضمان الأداء الأمثل لقاعدة البيانات، يجب إنشاء فهارس مناسبة على الحقول المستخدمة بكثرة في الاستعلامات.

### 7.1 الفهارس الأساسية

```sql
-- فهارس المستخدمين
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_is_active ON users(is_active);

-- فهارس الأدوار
CREATE INDEX idx_roles_parent_role_id ON roles(parent_role_id);
CREATE INDEX idx_roles_level ON roles(level);
CREATE INDEX idx_roles_is_active ON roles(is_active);

-- فهارس تعيين الأدوار
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
CREATE INDEX idx_user_roles_status ON user_roles(status);

-- فهارس المشاريع
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_project_manager_id ON projects(project_manager_id);
CREATE INDEX idx_projects_start_date ON projects(start_date);
CREATE INDEX idx_projects_end_date ON projects(end_date);

-- فهارس المهام
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_parent_task_id ON tasks(parent_task_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

### 7.2 الفهارس المركبة

```sql
-- فهارس مركبة للاستعلامات المعقدة
CREATE INDEX idx_user_roles_user_status ON user_roles(user_id, status);
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX idx_costs_project_date ON costs(project_id, date_incurred);
CREATE INDEX idx_metrics_project_date ON metrics(project_id, measurement_date);
```

## 8. قيود قاعدة البيانات

لضمان تكامل البيانات وصحتها، يجب تطبيق قيود مناسبة على قاعدة البيانات.

### 8.1 القيود الأساسية

```sql
-- قيود الفرادة
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
ALTER TABLE users ADD CONSTRAINT unique_username UNIQUE (username);
ALTER TABLE contracts ADD CONSTRAINT unique_contract_number UNIQUE (contract_number);

-- قيود التحقق
ALTER TABLE users ADD CONSTRAINT check_experience_level 
    CHECK (experience_level IN ('junior', 'mid', 'senior', 'expert'));

ALTER TABLE projects ADD CONSTRAINT check_status 
    CHECK (status IN ('planning', 'active', 'on_hold', 'completed', 'cancelled'));

ALTER TABLE tasks ADD CONSTRAINT check_priority 
    CHECK (priority IN ('low', 'medium', 'high', 'critical'));

ALTER TABLE tasks ADD CONSTRAINT check_progress_percentage 
    CHECK (progress_percentage >= 0 AND progress_percentage <= 100);
```

### 8.2 القيود المرجعية

```sql
-- المراجع الخارجية
ALTER TABLE user_roles ADD CONSTRAINT fk_user_roles_user_id 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE user_roles ADD CONSTRAINT fk_user_roles_role_id 
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE;

ALTER TABLE tasks ADD CONSTRAINT fk_tasks_project_id 
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

ALTER TABLE tasks ADD CONSTRAINT fk_tasks_assigned_to 
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE costs ADD CONSTRAINT fk_costs_project_id 
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;
```

## 9. استراتيجيات التحسين

لضمان الأداء الأمثل للنظام، يجب تطبيق استراتيجيات تحسين مختلفة على مستوى قاعدة البيانات والتطبيق.

### 9.1 تحسين الاستعلامات

**استخدام الفهارس بكفاءة:** يجب التأكد من أن جميع الاستعلامات المتكررة تستخدم الفهارس المناسبة. يمكن استخدام أدوات تحليل الأداء لتحديد الاستعلامات البطيئة وتحسينها.

**تجنب الاستعلامات المعقدة:** يفضل تقسيم الاستعلامات المعقدة إلى استعلامات أبسط متعددة، خاصة عند التعامل مع الجداول الكبيرة.

**استخدام التخزين المؤقت:** يمكن استخدام Redis لتخزين نتائج الاستعلامات المتكررة مؤقتًا، مما يقلل من الحمل على قاعدة البيانات.

### 9.2 تقسيم البيانات

**التقسيم الأفقي:** يمكن تقسيم الجداول الكبيرة مثل المهام والتكاليف حسب التاريخ أو المشروع لتحسين الأداء.

**التقسيم العمودي:** يمكن فصل البيانات نادرة الاستخدام إلى جداول منفصلة لتقليل حجم الجداول الرئيسية.

### 9.3 النسخ الاحتياطي والاستعادة

**النسخ الاحتياطي المجدول:** يجب إنشاء نسخ احتياطية منتظمة من قاعدة البيانات لضمان عدم فقدان البيانات.

**اختبار الاستعادة:** يجب اختبار عمليات الاستعادة بانتظام للتأكد من صحة النسخ الاحتياطية.

## 10. الأمان وحماية البيانات

حماية البيانات أمر بالغ الأهمية في نظام إدارة المشاريع، خاصة عند التعامل مع معلومات حساسة مثل البيانات المالية ومعلومات العملاء.

### 10.1 تشفير البيانات

**تشفير البيانات الحساسة:** يجب تشفير كلمات المرور والمعلومات المالية والبيانات الشخصية الحساسة قبل تخزينها في قاعدة البيانات.

**تشفير الاتصالات:** يجب استخدام SSL/TLS لتشفير جميع الاتصالات بين التطبيق وقاعدة البيانات.

### 10.2 التحكم في الوصول

**مستويات الوصول:** يجب تطبيق مستويات وصول مختلفة حسب الدور والمسؤوليات.

**تسجيل العمليات:** يجب تسجيل جميع العمليات الحساسة مثل تعديل البيانات المالية أو تغيير الأدوار.

### 10.3 التدقيق والمراجعة

**سجلات التدقيق:** يجب الاحتفاظ بسجلات مفصلة لجميع العمليات المهمة لأغراض التدقيق والمراجعة.

**المراجعة الدورية:** يجب إجراء مراجعات دورية للصلاحيات والوصول للتأكد من عدم وجود انتهاكات أمنية.

## الخلاصة

تصميم قاعدة البيانات المقترح يوفر أساسًا قويًا ومرنًا لنظام إدارة المشاريع الشامل. النماذج المصممة تدعم جميع المتطلبات المحددة بما في ذلك التفرع الهرمي للأدوار، إدارة المشاريع والمهام، التكاليف والعقود، مع تركيز خاص على مشاريع الذكاء الاصطناعي. الفهارس والقيود المقترحة تضمن الأداء الأمثل وتكامل البيانات، بينما استراتيجيات الأمان تحمي البيانات الحساسة وتضمن الامتثال للمعايير الأمنية.

