"""
Module that contains Ticket class
"""
from copy import deepcopy
from ..model.model_base import ModelBase

class dict_or_list():
    def typecast(self, input_string):
        try:
            if type(input_string) in [list, dict]:
                return input_string
            if isinstance(input_string, str):
                if input_string.strip() == '': return []
            if isinstance(eval(input_string), dict):
                return eval(input_string)
            if isinstance(eval(input_string), tuple):
                return list(eval(input_string))
            if isinstance(eval(input_string), int):
                return [eval(input_string)]
        except:
            raise Exception('Input is required to be list or dict in string format')

class Ticket(ModelBase):
    """
    Ticket allows to create multiple similar RelVals in the same campaign
    """

    _ModelBase__schema = {
        # Database id (required by database)
        '_id': '',
        # PrepID
        'prepid': '',
        # Batch name
        'batch_name': '',
        # CMSSW release
        'cmssw_release': '',
        # Jira ticket 
        'jira_ticket': '',
        # Title/Purpose of the validation
        'title': '',
        # CMS-Talk link 
        'cms_talk_link': '',
        # Custom HLT Menu
        'hlt_menu': '',
        # HLT GT
        'hlt_gt': '',
        # Prompt GT
        'prompt_gt': '',
        # Express GT
        'express_gt': '',
        # Common Prompt GT for HLT
        'common_prompt_gt_for_hlt': '',
        # Common Prompt GT for HLT Ref
        'common_prompt_gt_for_hlt_ref':'',
        # HLT reference GT
        'hlt_gt_ref': '',
        # Prompt reference GT
        'prompt_gt_ref': '',
        # Express reference GT
        'express_gt_ref': '',
        # Attached workflows to HLT, Prompt, Express
        'attached_wfs': {'HLT': [], 'Prompt': [], 'Express': []},
        # Additional command to add to all cmsDrivers
        'command': '',
        # List of steps that additional command should be applied to
        'command_steps': [],
        # CPU cores
        'cpu_cores': 1,
        # List of prepids of relvals that were created from this ticket
        'created_relvals': [],
        # GPU parameters that will be added to selected steps
        'gpu': {'requires': 'forbidden',
                'gpu_memory': '',
                'cuda_capabilities': [],
                'cuda_runtime': '',
                'gpu_name': '',
                'cuda_driver_version': '',
                'cuda_runtime_version': ''},
        # List of steps that GPU parameters should be applied to
        'gpu_steps': [],
        # Action history
        'history': [],
        # Label to be used in runTheMatrix
        'label': '',
        # Type of relval: standard, upgrade, premix, etc.
        'matrix': 'standard',
        # Memory in MB
        'memory': 2000,
        # User notes
        'notes': '',
        # nStreams to be used in all steps, 0 defaults to nThreads
        'n_streams': 0,
        # Whether to recycle first step
        'recycle_gs': False,
        # Which step should be first that run while recycling the input
        'recycle_input_of': '',
        # String to rewrite middle part of INPUT dataset(s) /.../THIS/...
        'rewrite_gt_string': '',
        # Tag to group workflow ids
        'sample_tag': '',
        # Overwrite default scram arch
        'scram_arch': '',
        # Status is either new or done
        'status': 'new',
        # Workflow ids
        'workflow_ids': [],
        # Input datasets
        'input_datasets': [],
        # Input runs
        'input_runs': dict_or_list(),
    }

    lambda_checks = {
        'prepid': lambda prepid: ModelBase.matches_regex(prepid, '[a-zA-Z0-9_\\-]{1,75}'),
        'batch_name': ModelBase.lambda_check('batch_name'),
        'cmssw_release': ModelBase.lambda_check('cmssw_release'),
        'cpu_cores': ModelBase.lambda_check('cpu_cores'),
        '__created_relvals': ModelBase.lambda_check('relval'),
        '_gpu': {
            'requires': lambda r: r in ('forbidden', 'optional', 'required'),
            'cuda_capabilities': lambda l: isinstance(l, list),
            'gpu_memory': lambda m: m == '' or int(m) > 0,
         },
        'label': ModelBase.lambda_check('label'),
        'matrix': ModelBase.lambda_check('matrix'),
        'memory': ModelBase.lambda_check('memory'),
        'n_streams': lambda streams: 0 <= streams <= 16,
        'rewrite_gt_string': lambda rgs: ModelBase.matches_regex(rgs, '[a-zA-Z0-9\\.\\-_]{0,199}'),
        'sample_tag': ModelBase.lambda_check('sample_tag'),
        'hlt_gt': ModelBase.lambda_check('globaltag'),
        'prompt_gt': ModelBase.lambda_check('globaltag'),
        'express_gt': ModelBase.lambda_check('globaltag'),
        'common_prompt_gt_for_hlt': ModelBase.lambda_check('globaltag'),
        'common_prompt_gt_for_hlt_ref': ModelBase.lambda_check('globaltag'),
        'status': lambda status: status in ('new', 'done'),
        'scram_arch': lambda s: not s or ModelBase.lambda_check('scram_arch')(s),
        'workflow_ids': lambda wf: len(wf) > 0,
        '__workflow_ids': lambda wf: wf > 0,
        '__input_datasets': lambda ds: len(ds) >= 0,
        '___input_runs': lambda ir: len(ir) >= 0,

    }

    def __init__(self, json_input=None, check_attributes=True):
        if json_input:
            json_input = deepcopy(json_input)
            json_input['workflow_ids'] = [float(wid) for wid in json_input['workflow_ids']]
            json_input['recycle_gs'] = bool(json_input.get('recycle_gs', False))
            if json_input.get('gpu', {}).get('requires') not in ('optional', 'required'):
                json_input['gpu'] = self.schema().get('gpu')
                json_input['gpu']['requires'] = 'forbidden'
                json_input['gpu_steps'] = []

        ModelBase.__init__(self, json_input, check_attributes)
