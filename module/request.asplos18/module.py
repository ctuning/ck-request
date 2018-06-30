#
# Collective Knowledge: CK-powered AI/SW/HW co-design for ReQuEST tournaments
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, cTuning foundation/dividiti
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

repo_with_validated_results='ck-request-asplos18-results'

# Local settings
line='================================================================'

form_name='request_web_form'
onchange='document.'+form_name+'.submit();'

hextra='<center>\n'
hextra+='<p>\n'
hextra+=' Beta scoreboard for <a href="http://cknowledge.org/request-cfp-asplos2018.html">ReQuEST@ASPLOS\'18 AI/SW/HW co-design competition</a>\n'
hextra+=' (see <a href="https://doi.org/10.1145/3229762">ACM proceedings</a> and <a href="https://portalparts.acm.org/3230000/3229762/fm/frontmatter.pdf">results report</a>).\n'

#hextra+=' (your <a href="https://github.com/ctuning/ck-request/issues">feedback</a>)\n'
hextra+='</center>\n'
hextra+='<p>\n'

selector=[
          {'name':'Results', 'key':'results', 'skip_update':'yes', 'new_line_after':'yes', 'skip_from_reset':'yes'}, # need to skip from reset to be able to get values from other repos
          {'name':'Algorithm species', 'key':'algorithm_species', 'module_uoa':'1702c3e426ca54c5'},
#          {'name':'Competition', 'key':'scenario_module_uoa', 'module_uoa':'032630d041b4fd8a'},
          {'name':'Model species', 'key':'model_species', 'module_uoa':'38e7de41acb41d3b'},
          {'name':'Precision', 'key':'model_precision'},
          {'name':'Dataset species', 'key':'dataset_species', 'new_line':'yes', 'keep_empty':'yes'},
          {'name':'Dataset size', 'key':'dataset_size', 'type':'int'},
          {'name':'Cloud/farm', 'key':'farm', 'new_line':'yes', 'keep_empty':'yes'},
          {'name':'Platform species', 'key':'platform_species'},
          {'name':'Platform', 'key':'plat_name'},
          {'name':'OS name', 'key':'os_name', 'new_line':'yes'},
          {'name':'CPU name', 'key':'cpu_name', 'keep_empty':'yes'},
          {'name':'GPGPU name', 'key':'gpgpu_name', 'keep_empty':'yes'}
         ]

selector2=[
           {'name':'Algorithm implementation (CK program)', 'key':'##choices#data_uoa#min'},
           {'name':'Model design', 'key':'##meta#model_design_name'},
           {'name':'Compiler', 'key':'##meta#compiler_name','new_line':'yes', 'keep_empty':'yes'},
           {'name':'Library/framework', 'key':'##meta#library_name', 'keep_empty':'yes'},
           {'name':'OpenCL driver', 'key':'##features#gpgpu@0#gpgpu_misc#opencl c version#min', 
                              'extra_key':'##features#gpgpu@0#gpgpu_misc#opencl_c_version#min', 'new_line':'yes', 'keep_empty':'yes'},
           {'name':'Batch size', 'key':'##features#batch_size#min','type':'int', 'new_line':'yes'},
           {'name':'CPU freq (MHz)', 'key':'##features#cpu_freq#min','type':'int', 'keep_empty':'yes'},
           {'name':'GPU freq (MHz)', 'key':'##features#gpu_freq#min','type':'int', 'keep_empty':'yes'},
           {'name':'Freq (MHz)', 'key':'##features#freq#min','type':'int', 'keep_empty':'yes'}
          ]

selector3=[
           {'name':'Plot dimension 1 (X)', 'key':'plot_dimension1'},
           {'name':'Show variation', 'key':'plot_variation_dimension1',  'new_line_after':'yes'},
           {'name':'Plot dimension 2 (Y)', 'key':'plot_dimension2'},
           {'name':'Show variation', 'key':'plot_variation_dimension2',  'new_line_after':'yes'}
          ]

k_hi_uid='highlight_behavior_uid'
k_hi_user='highlight_by_user'
k_view_all='all'

hidden_keys=[k_hi_uid, k_hi_user, k_view_all]

dimensions=[
             {"key":"experiment", "name":"Experiment number", "skip_from_cache":"yes"},
             {"key":"##characteristics#run#prediction_time_avg_s", "name":"Prediction time per 1 image (min, sec.)"},
             {"key":"##characteristics#run#inference_latency", "name":"Inference latency for 1 image (min, sec.)"},
             {"key":"##characteristics#run#inference_throughput", "name":"Inference throughput (max, images per sec.)", "reverse":"yes"},
             {"key":"##characteristics#run#accuracy_top1", "name":"Accuracy on all images (Top1)"},
             {"key":"##characteristics#run#accuracy_top5", "name":"Accuracy on all images (Top5)"},
             {"key":"##features#model_size", "name":"Model size (B)"},
             {"key":"##meta#platform_peak_power", "name":"Platform peak power (W)", "from_meta":"yes"},
             {"key":"##meta#platform_price", "name":"Platform price ($)", "from_meta":"yes"},
             {"key":"##characteristics#run#usage_cost", "name":"Usage cost ($)"},
             {"key":"##meta#platform_species", "name":"Platform species", "from_meta":"yes"},
             {"key":"##meta#model_species", "name":"Model species", "from_meta":"yes", 'module_uoa':'38e7de41acb41d3b'},
             {"key":"##meta#model_precision", "name":"Model precision", "from_meta":"yes"},
             {"key":"##meta#dataset_species", "name":"Dataset species", "from_meta":"yes"},
             {"key":"##features#freq", "name":"Device frequency (MHz)"},
             {"key":"##features#cpu_freq", "name":"CPU frequency (MHz)"},
             {"key":"##features#gpu_freq", "name":"GPU frequency (MHz)"},
             {"key":"##features#batch_size", "name":"Batch size"}
           ]

# Only from points (not from entry meta!)
view_cache=[
  "##choices#data_uoa#min",
  "##choices#env#*#min",
  "##pipeline_state#fail_bool#min",
  "##pipeline_state#fail_reason#min",
  "##characteristics#compile#compilation_success_bool#min",
  "##characteristics#run#run_success_bool#min",
  "##characteristics#run#output_check_failed_bool#min",
  "##characteristics#run#execution_time#min",
  "##characteristics#run#execution_time#max",
  "##features#cpu_freq#min",
  "##features#gpu_freq#min",
  "##features#freq#min",
  "##features#batch_size#min",
  "##features#gpgpu@0#gpgpu_misc#opencl c version#min"
]

table_view=[
  {"key":"##meta#algorithm_species", "name":"Algorithm species", 'module_uoa':'1702c3e426ca54c5', "skip_if_key_in_input":"algorithm_species"},
  {"key":"##choices#data_uoa#min", "name":"Workload (program,model,library)", "skip_if_the_same_key_in_input":"yes"},
  {"key":"##meta#model_species", "name":"Model species", 'module_uoa':'38e7de41acb41d3b', "skip_if_key_in_input":"model_species"},
  {"key":"##meta#model_precision", "name":"Precision", "skip_if_key_in_input":"model_precision"},
  {"key":"##meta#dataset_species", "name":"Dataset species", "skip_if_key_in_input":"dataset_species"},
  {"key":"##meta#dataset_size", "name":"Dataset size", "skip_if_key_in_input":"dataset_size", "type":"int"},
  {"key":"##meta#farm", "name":"Farm", "skip_if_key_in_input":"farm"},
  {"key":"##meta#platform_species", "name":"Platform species", "skip_if_key_in_input":"platform_species"},
  {"key":"##meta#plat_name", "name":"Platform name", "skip_if_key_in_input":"plat_name"},
  {'key':'##meta#cpu_name', 'name':'CPU name', "skip_if_key_in_input":"cpu_name"},
  {"key":"##features#cpu_freq#min", "name":"CPU freq (MHz)", "skip_if_the_same_key_in_input":"yes"},
  {'key':'##meta#gpgpu_name', 'name':'GPGPU name', "skip_if_key_in_input":"gpgpu_name"},
  {"key":"##features#gpu_freq#min", "name":"GPU freq (MHz)", "skip_if_the_same_key_in_input":"yes"},
  {'key':'##meta#os_name', 'name':'OS name', "skip_if_key_in_input":"os_name"},
  {"key":"##meta#versions", "name":"SW deps and versions", "json_and_pre":"yes", "align":"left"},
  {"key":"##meta#model_design_name", "name":"Model design", "skip_if_the_same_key_in_input":"yes"},
  {"key":"##meta#compiler_name", "name":"Compiler", "skip_if_the_same_key_in_input":"yes"},
  {"key":"##meta#library_name", "name":"Library", "skip_if_the_same_key_in_input":"yes"},
  {"key":"##choices#env#", "name":"Environment", "starts_with":"yes", "align":"left"},
  {"key":"##characteristics#run#prediction_time_avg_s#min", "name":"Classification time per 1 image (sec. min/max)", "check_extra_key":"max", "format":"%.4f"},
  {"key":"##characteristics#run#inference_latency#min", "name":"Inference latency for 1 image (min, sec.)", "check_extra_key":"max", "format":"%.4f"},
  {"key":"##characteristics#run#inference_throughput#max", "name":"Inference throughput (max, images per sec.)", "check_extra_key":"min", "format":"%.1f"},
  {"key":"##extra#accuracy_sum", "name":"Accuracy (Top1&nbsp;/&nbsp;Top5)"},
  {"key":"##features#batch_size#min", "name":"Batch size"},
  {"key":"##features#model_size#min", "name":"Model size (B)"},
  {"key":"##features#memory_usage#min", "name":"Memory usage (B)"},
  {"key":"##meta#platform_peak_power", "name":"Platform peak power (W)", "check_extra_key":"max", "format":"%.3f"},
  {"key":"##meta#platform_price_str", "name":"Platform price ($)"},
  {"key":"##characteristics#run#usage_cost#min", "name":"Usage cost per image ($)", "type":"float", "format":"%.2e"},
  {"key":"##extra#html_reproducibility", "name":"Reproducibility", "align":"left"}
]

artifacts={}
artifacts_cache={}

prune_first_level=100
prune_second_level=400

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# show results

def show(i):
    """
    Input:  {
               (crowd_module_uoa)       - if rendered from experiment crowdsourcing
               (crowd_key)              - add extra name to Web keys to avoid overlapping with original crowdsourcing HTML
               (crowd_on_change)        - reuse onchange doc from original crowdsourcing HTML

               (highlight_behavior_uid) - highlight specific result (behavior)!
               (highlight_by_user)      - highlight all results from a given user

               (refresh_cache)          - if 'yes', refresh view cache
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import copy
    import time
    import json

    # Preparing various parameters to render HTML dashboard
    st=''

    view_all=i.get(k_view_all,'')

    cmuoa=i.get('crowd_module_uoa','')
    ckey=i.get('crowd_key','')

    wchoices3={
            ckey+'plot_dimension1':[],
            ckey+'plot_variation_dimension1':[{'name':'no', 'value':'no'}, {'name':'yes', 'value':'yes'}],
            ckey+'plot_dimension2':[],
            ckey+'plot_variation_dimension2':[{'name':'no', 'value':'no'}, {'name':'yes', 'value':'yes'}]
          }

    if i.get(ckey+'plot_dimension1','')=='': i[ckey+'plot_dimension1']=dimensions[3]['key']
    if i.get(ckey+'plot_dimension2','')=='': i[ckey+'plot_dimension2']=dimensions[4]['key']

    if 'reset_'+form_name in i: reset=True
    else: reset=False

    if 'all_choices_'+form_name in i: all_choices=True
    else: all_choices=False

    debug=(i.get('debug','')=='yes')
#    debug=True

    conc=i.get('crowd_on_change','')
    if conc=='':
        conc=onchange

    hi_uid=i.get(k_hi_uid,'')
    hi_user=i.get(k_hi_user,'')

    refresh_cache=i.get('refresh_cache','')

    if 'refresh_cache_'+form_name in i: 
       refresh_cache='yes'

    bd='<div style="background-color:#bfffbf;margin:5px;">'

#    h='<hr>\n'
    h='<center>\n'

    h+='\n\n<script language="JavaScript">function copyToClipboard (text) {window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);}</script>\n\n' 

    h+=hextra

#    h+='<hr>\n'
#    h+='<br>\n'

    # Check host URL prefix and default module/action *********************************************
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe',
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']
    template=rx['template']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # Check and add hidden keys ***************************************************
    h+='\n\n'

    for k in hidden_keys:
        if i.get(k,'')!='':
           h+='<input type="hidden" name="'+k+'" value="'+i[k]+'">\n'

    h+='\n\n'

    # Check repos
    experiment_tags='request-asplos18'
    experiment_repos=['ck-request', repo_with_validated_results]

    # only selected repo (to simplify analysis)
#    experiment_repos=[]

    x=i.get(ckey+'results','')
    if x=='all':
       experiment_repos=[]
    elif x=='local':
       experiment_repos.append('local')
    elif x!='':
       experiment_repos.append(x)

    # Prepare first level of selection with pruning ***********************************************
    r=ck.access({'action':'prepare_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'original_input':i,
                 'tags':experiment_tags,
                 'search_repos':experiment_repos,
                 'debug': debug,
                 'selector':selector,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'url1':url1,
                 'form_name':form_name,
                 'background_div':bd,
                 'skip_html_selector':'yes'})
    if r['return']>0: return r

    olst=r['lst'] # original list (if all_choices)
    plst=r['pruned_lst']

    # Compose extra meta (such as deps, versions, etc)
    plst1=[]
    for q in plst:
        duid=q['data_uid']

        meta=q['meta']['meta']

        if meta.get('processed','')!='yes':
           continue

        ds=meta.get('deps_summary',{})

        xds={}

        ver=json.dumps(ds, indent=2, sort_keys=True)
        ver1=''

        for k in sorted(ds):
            x=ds[k]

            r=make_deps_full_name({'deps':x})
            if r['return']>0: return r

            y=r['full_name']
            x['full_name']=y

            ver1+='<b>'+k+'</b>: '+str(y)+'<br>\n'

#        dver=meta.get('engine_meta',{}).get(cpu_abi,{})
#        ver+='main: '+str(dver.get('program_version',''))+'\n'
#        dps=dver.get('deps_versions',{})
#        for dx in dps:
#            ver+=dx+': '+str(dps[dx].get('version',''))+'\n'

        ver=ver.replace("\'","'").replace("'","\\'").replace('\"','"').replace('"',"\\'").replace('\n','\\n')
        if ver!='':
            ver='<center><input type="button" class="ck_small_button" onClick="alert(\''+ver+'\');" value="View json"></center>\n'

        ver+='<br>'+ver1

        meta['versions']=ver

        x=meta.get('platform_price','')
        if x!='':
           x=str(x)
           y=meta.get('platform_price_date','')
           if y!='':
              x+=' <i>('+y+')</i>'
           meta['platform_price_str']=x

        # Artifact info
        auoa=meta.get('artifact','')
        if auoa!='' and artifacts.get(duid,'')=='':
           x=artifacts_cache.get(auoa,'')

           if x=='':
              amuoa=cfg['module_deps']['artifact']
              r=ck.access({'action':'load',
                           'module_uoa':amuoa,
                           'data_uoa':auoa})
              if r['return']==0:
                 dx=r['dict']
                 ap=r['path']

                 # Check repos
                 repos=dx.get('repos',[])
                 if len(repos)>0:
                    x='<b>Repositories</b><br>\n'
                    x+='<div style="margin:7px;">\n'
                    for a in repos:
                        n=a['name']
                        u=a['url']
                        x+='<a href="'+u+'">'+n+'</a><br>\n'
                    x+='</div>\n'

                 # Check interactive report
                 ir=dx.get('interactive_report','')
                 if ir!='':
                    u=url0+'wcid='+cfg['module_deps']['report']+':'+ir

                    x+='<p><b>Report</b><br>\n'
                    x+='<div style="margin:7px;">\n'
                    x+='<a href="'+u+'" target="_blank">Interactive</a>\n'
                    x+='</div>\n'

                 # Check DOIs
                 dois=dx.get('dois',[])
                 if len(dois)>0:
                    x+='<p><b>DOIs</b><br>\n'
                    x+='<div style="margin:7px;">\n'
                    for a in dois:
                        n=a['name']
                        u=a['url']
                        x+='<a href="'+u+'">'+n+'</a><br>\n'
                    x+='</div>\n'

                 # Check ACM badges
                 y=''
                 acm=dx.get('acm_badges',{})

                 if acm.get('available','')=='yes':
                    y='available'

                 if acm.get('reusable','')=='yes':
                    if y!='':y+=', '
                    y+='reusable'
                 elif acm.get('functional','')=='yes':
                    if y!='':y+=', '
                    y='functional'

                 if acm.get('replicated','')=='yes':
                    if y!='':y+=', '
                    y+='replicated'
                 elif acm.get('replicated','')=='yes':
                    if y!='':y+=', '
                    y+='reproduced'

                 if y!='':
                    x+='<p><b>ACM badges</b><br>\n'
                    x+='<div style="margin:7px;">\n'
                    x+=y+'<br>\n'
                    x+='</div>\n'

                 # Check review
                 apf='review.html'
                 apr=os.path.join(ap,apf)
                 if os.path.isfile(apr):
                    u=url0+'action=pull&common_action=yes&cid='+amuoa+':'+auoa+'&filename='+apf

                    x+='<p><b>Review</b><br>\n'
                    x+='<div style="margin:7px;">\n'
                    x+=' See <a href="'+u+'" target="_blank">notes</a>\n'
                    x+='</div>\n'

                    x+='</div>\n'

                 # Check extra HTML
                 y=dx.get('html','')
                 if y!='':
                    x+='<p>'+y+'<br>\n'

              x+='<p>\n'

           artifacts[duid]=x   

        plst1.append(q)

    plst=plst1

    # Sort list ***********************************************************************************
    dt=time.time()
    splst=plst
#        sorted(plst, key=lambda x: (
#        x.get('meta',{}).get('meta',{}).get('prog_uoa',''), 
#        x.get('meta',{}).get('meta',{}).get('dataset_uoa',''), 
#        x.get('meta',{}).get('meta',{}).get('plat_name',''), 
#        x.get('meta',{}).get('meta',{}).get('timestamp','')
#        ))
#
#    if debug: h+='\n<p>Debug time (sorting table): '+str(time.time()-dt)+' sec.<p>\n'

    # Prune list **********************************************************************************
    len_splst=len(splst)
    if len_splst>prune_first_level:
       splst=splst[:prune_first_level]

       h+='\n<i>Showing '+str(prune_first_level)+' of '+str(len_splst)+' entries ...</i><br>\n'

    # Prepare and cache results for the table
    for dim in dimensions:
        k=dim['key']

        if dim.get('skip_from_cache','')!='yes':
           if dim.get('from_meta','')=='yes':
              if k not in view_cache:
                 view_cache.append(k)
           else:
              k1=k+'#min'
              if k1 not in view_cache:
                 view_cache.append(k1)
              k2=k+'#max'
              view_cache.append(k2)

    r=ck.access({'action':'get_and_cache_results',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'lst':splst,
                 'cache_uid':work['self_module_uid'],
                 'refresh_cache':refresh_cache,
                 'view_cache':view_cache,
                 'table_view':table_view})
    if r['return']>0: return 
    table=r['table']

    # Prepare second level of selection with pruning ***********************************************
    r=ck.access({'action':'prepare_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'original_input':i,
                 'tags':experiment_tags,
                 'search_repos':experiment_repos,
                 'lst':table,
                 'skip_meta_key':'yes',
                 'debug': debug,
                 'selector':selector2,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'url1':url1,
                 'form_name':form_name,
                 'skip_form_init':'yes',
                 'background_div':bd})
    if r['return']>0: return r

    h2=r['html']
    table=r['pruned_lst']

    choices2=r['choices']
    wchoices2=r['wchoices']

    # Extra fields (customized for this module) *****************************************************************************
    for row in table:
        duoa=row.get('##data_uid','')
        dpoint=row.get('##point_uid','')

        # Replay
        x=''
        if duoa!='' and dpoint!='':
           x='ck replay experiment:'+duoa+' --point='+str(dpoint)
           y=ck.cfg.get('add_extra_to_replay','')
           if y!='':x+=' '+y

        xh='<p><input type="button" class="ck_small_button" onClick="copyToClipboard(\''+x+'\');" value="CK replay">\n'

        # Move to validated
        x=''
        if duoa!='' and dpoint!='':
           x='ck validate request.asplos18 --experiment='+duoa+' --point='+str(dpoint)

        xh+='<p><input type="button" class="ck_small_button" onClick="copyToClipboard(\''+x+'\');" value="Validate">\n'

        xh=artifacts.get(duoa,'')+xh

        row['##extra#html_reproducibility']=xh

        # Accuracy sum (Top1/Top5)
        x=''

        x1=row.get('##characteristics#run#accuracy_top1#min','')
        x2=row.get('##characteristics#run#accuracy_top5#min','')

        if x1!='':
           x='%.3f' % x1
        if x2!='':
           x+='&nbsp;/&nbsp;'
           x+='%.3f' % x2

        row['##extra#accuracy_sum']=x

        # Images per second
        t=row.get('##characteristics#run#prediction_time_avg_s#min','')
        if t!=None and t!='':
           ips=1/t
           row['images_per_second']=ips

    # Prune first list based on second selection*****************************************************************************
    if all_choices:
       nsplst=olst
    elif reset:
       nsplst=splst
    else:
       all_uid=[]
       for row in table:
           duid=row.get('##data_uid','')
           if duid!='' and duid not in all_uid:
              all_uid.append(duid)

       nsplst=[]
       for q in splst:
           if q['data_uid'] in all_uid:
              nsplst.append(q)

    # Check if too many *****************************************************************************************************
    ltable=len(table)
    min_view=False

    hx=''
    if ltable==0:
       hx='\n<b>No results found!</b>'
#        return {'return':0, 'html':h, 'style':st}

    elif ltable>prune_second_level and view_all!='yes':
       table=table[:prune_second_level]

       hx='\n<i>Showing '+str(prune_second_level)+' of '+str(ltable)+' entries ...</i><br>\n'

    # Get unique values and create html selector 1 (after selector 2)
    r=ck.access({'action':'get_unique_keys_from_list',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'lst':nsplst,
                 'selector':selector,
                 'crowd_key':ckey,
                 'original_input':i})
    if r['return']>0: return 

    choices1=r['choices']
    wchoices1=r['wchoices']

    # Check results from papers
    x=[
       {"name":"only validated","value":""},
#       {"name":"all","value":"all"},
       {"name":"local","value":"local"},
       {"name":"for ReQuEST@ASPLOS'18 workflow \"mobilenets-armcl-opencl\"","value":"ck-request-asplos18-results-mobilenets-armcl-opencl"},
       {"name":"for ReQuEST@ASPLOS'18 worklfow \"caffe-intel\"","value":"ck-request-asplos18-results-caffe-intel"},
       {"name":"for ReQuEST@ASPLOS'18 workflow \"mobilenets-tvm-arm\"","value":"ck-request-asplos18-results-mobilenets-tvm-arm"},
       {"name":"for ReQuEST@ASPLOS'18 workflow \"iot-farm\"","value":"ck-request-asplos18-results-iot-farm"},
       {"name":"for ReQuEST@ASPLOS'18 workflow \"resnet-tvm-fpga\"","value":"ck-request-asplos18-results-resnet-tvm-fpga"}
      ]
    wchoices1[ckey+'results']=x

    # Prepare selector 1  (based on choices from selector 2)
    r=ck.access({'action':'prepare_html_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'start_form':'yes',
                 'url1':url1,
                 'form_name':form_name,
                 'background_div':bd,
                 'selector':selector,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'wchoices':wchoices1,
                 'original_input':i})
    if r['return']>0: return r
    h1=r['html']

    h+=h1+'\n'+h2

    ltable=len(table)
    min_view=False

    if ltable==0:
       h+=''
#        h+='<b>No results found!</b>'
#        return {'return':0, 'html':h, 'style':st}

    elif ltable>prune_second_level and view_all!='yes':
       table=table[:prune_second_level]

       h+='\n<i>Showing '+str(prune_second_level)+' of '+str(ltable)+' entries ...</i><br>\n'

    # Prepare selector 3 (without pruning - about tables and graphs)
    arc='yes'
    if ck.cfg.get('request_skip_refresh_cache_button','')=='yes': arc=''

    # Prepare dimensions
    for dim in dimensions:
        k=dim['key']
        n=dim['name']

        wchoices3[ckey+'plot_dimension1'].append({'name':n, 'value':k})
        wchoices3[ckey+'plot_dimension2'].append({'name':n, 'value':k})

    r=ck.access({'action':'prepare_html_selector',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'start_form':'no',
                 'url1':url1,
                 'form_name':form_name,
                 'background_div':bd,
                 'selector':selector3,
                 'crowd_key':ckey,
                 'crowd_on_change':conc,
                 'wchoices':wchoices3,
                 'original_input':i,
                 'add_refresh_cache':arc,
                 'add_reset':'yes'})
    if r['return']>0: return r
    h+='\n'+r['html']+'\n'

    h+='\n'+hx+'\n'

    if ltable==0:
        return {'return':0, 'html':h, 'style':st}

    # Prepare graph *********************************************************************************************************
    bgraph={'0':[], '1':[]}
    igraph={'0':[], '1':[]}

#    stable=sorted(table, key=lambda row: (
#        ck.safe_float(row.get('##characteristics#run#execution_time#min',None),0.0)
#        ))

    ix=0

    kdim1=i.get(ckey+'plot_dimension1','')
    kvdim1=i.get(ckey+'plot_variation_dimension1','')
    kdim2=i.get(ckey+'plot_dimension2','')
    kvdim2=i.get(ckey+'plot_variation_dimension2','')

    # Find X/Y names
    ndim1=''
    ndim2=''
    dim1_from_meta=False
    dim2_from_meta=False
    dim1_module=''
    dim2_module=''
    dim1_reverse=''
    dim2_reverse=''

    for k in dimensions:
        kk=k['key']
        kn=k['name']

        if kk==kdim1: 
           ndim1=kn
           if k.get('from_meta','')=='yes':
              dim1_from_meta=True
           dim1_module=k.get('module_uoa','')
           dim1_reverse=k.get('reverse','')

        if kk==kdim2: 
           ndim2=kn
           if k.get('from_meta','')=='yes':
              dim2_from_meta=True
           dim2_module=k.get('module_uoa','')
           dim2_reverse=k.get('reverse','')

    kdim1min=kdim1
    kdim2min=kdim2
    kdim1max=kdim1
    kdim2max=kdim2

    max1=0

    # Labels if not int and not float
    ldim1={}
    ldim2={}

    if not dim1_from_meta:
       if dim1_reverse!='yes':
          kdim1min+='#min'
          kdim1max+='#max'
       else:
          kdim1min+='#max'
          kdim1max+='#min'

    if not dim2_from_meta:
       if dim2_reverse!='yes':
          kdim2min+='#min'
          kdim2max+='#max'
       else:
          kdim2min+='#max'
          kdim2max+='#min'

    for row in table:
        ix+=1
        six=str(ix)

        if kdim1=='experiment': 
           dim1=ix
        else:
           v=row.get(kdim1min,None)
           if v==None or v=='': continue
           v=check_label(v, ldim1)
           dim1=v

        if dim1>max1: max1=dim1

        point=[dim1]

        if kdim1!='experiment' and kvdim1=='yes':
           v=row.get(kdim1max,None)
           if v==None or v=='': continue
           v=check_label(v, ldim1)
           dim1max=v

           delta=0.0
           if dim1!=0.0 and dim1max!=0.0:
              delta=abs(dim1max-dim1)

           if dim1_reverse!='yes':
              dm=dim1+delta
           else:
              dm=dim1-delta

           point.append(dm)

        if kdim2=='experiment': 
           dim2=ix
        else:
           v=row.get(kdim2min,None)
           if v==None or v=='': continue
           v=check_label(v, ldim2)
           dim2=v

        point.append(dim2)

        if kdim2!='experiment' and kvdim2=='yes':
           v=row.get(kdim2max,None)
           if v==None or v=='': continue
           v=check_label(v, ldim2)
           dim2max=v

           delta=0.0
           if dim2!=0.0 and dim2max!=0.0:
              delta=abs(dim2max-dim2)

           if dim2_reverse!='yes':
              dm=dim2+delta
           else:
              dm=dim2-delta

           point.append(dm)

        raw_data_url=url0#+'wcid='+x+':'+duid

        ind='0'
        ruoa=row.get('##repo_uoa','')

        if ruoa==repo_with_validated_results: ind='1'

        bgraph[ind].append(point)
        igraph[ind].append({'size':4, 'features':row, 'anchor':'id'+six})

#Old
#        igraph['0'].append({'size':sizem, 'color':xcol, 'features':row, 'url':'', 'url_ext':raw_data_url})
#        igraph['0'].append({'size':4, 'features':row, 'anchor':'id'+six}) #, 'url':'', 'url_ext':''})

    if len(bgraph['0'])>0 or len(bgraph['1'])>0:
       dt=time.time()
       ii={'action':'plot',
           'module_uoa':cfg['module_deps']['graph'],

           "table":bgraph,
           "table_info":igraph,

           "xmin":-(float(max1)/20),
           "ymin":0,

           "ignore_point_if_none":"yes",

           "plot_type":"d3_2d_scatter",

           "display_x_error_bar2":kvdim1,
           "display_y_error_bar2":kvdim2,

           "title":"Powered by Collective Knowledge",

           "x_ticks_period":10,

           "axis_x_desc": ndim1,
           "axis_y_desc": ndim2,

           "plot_grid":"yes",

           "d3_div":"ck_interactive",

           "point_style":{"1":{"color":"#0198E1", "connect_lines":"no"},
                          "0":{"color":"#dc3912", "connect_lines":"no"}},

           "image_width":"900",
           "image_height":"400",

           "wfe_url":url0}

       r=ck.access(ii)
       if r['return']==0:
          x=r.get('html','')
          if x!='':
             st+=r.get('style','')

             h+='<center>\n'
             h+='<div id="ck_box_with_shadow" style="width:940px;">\n'
             h+=' <div id="ck_interactive" style="text-align:center;font-size:11px;">\n'
             h+=x+'\n'
             h+=' </div>\n'
             h+='</div>\n'
             h+='</center>\n'
             h+='<br>\n'

             if len(ldim1)>0:
                r=html_labels({'labels':ldim1, 'axis':'X', 'module_uoa':dim1_module})
                if r['return']>0: return r
                h+=r['html']
             if len(ldim2)>0:
                r=html_labels({'labels':ldim2, 'axis':'Y', 'module_uoa':dim2_module})
                if r['return']>0: return r
                h+=r['html']
             h+='<br>\n'

    # In the future, we may want to use Django + numpy here
    # Prepare table header ******************************************************************
    bgc='dfffdf'
    bg=' style="background-color:#'+bgc+';"'
    bg1=' style="background-color:#bfffbf;"'
    bg2=' style="background-color:#afffaf;"'

    h+='<small><table border="1" cellpadding="7" cellspacing="0">\n'

    ha='align="$#align#$" valign="top"'

    # Prepare table header *****************************************************************
    h+='  <tr style="background-color:#dddddd">\n'

    h+='   <td '+ha.replace('$#align#$','center')+'><b>#</b></td>\n'

    for tv in table_view:
        k=tv['key']

        align=tv.get('align','')
        if align=='': align='center'

        skip=False

        kk=tv.get('skip_if_key_in_input','')
        if kk!='' and i.get(ckey+kk,'')!='':
           skip=True

        if not skip and tv.get('skip_if_the_same_key_in_input','')=='yes' and i.get(ckey+k,'')!='':
           skip=True

        if not skip:
           n=tv.get('name','')
           if n=='': n=k

           h+='   <td '+ha.replace('$#align#$',align)+'><b>'+n+'</b></td>\n'

    h+='  </tr>\n'

    # Draw table ***************************************************************************
    dt=time.time()
    ix=0
    for q in table:
        ix+=1
        six=str(ix)

        # Check colors
        bgx=bg
        bgx1=bg1
        bgx2=bg2
        if (hi_uid!='' and duid==hi_uid) or (hi_user!='' and hi_user==user):
           bgx=' style="background-color:#ffcf7f"'
           bgx1=' style="background-color:#ffbf5f"'
           bgx2=' style="background-color:#ffaf2f"'

        # Starting raw ***************************************
        h+='  <tr'+bgx+'>\n'

        h+='   <td '+ha.replace('$#align#$','center')+'><a name="id'+six+'" id="id'+six+'">'+six+'</a></td>\n'

        for tv in table_view:
            k=tv['key']

            align=tv.get('align','')
            if align=='': align='center'

            skip=False

            kk=tv.get('skip_if_key_in_input','')
            if kk!='' and i.get(ckey+kk,'')!='':
               skip=True

            if not skip and tv.get('skip_if_the_same_key_in_input','')=='yes' and i.get(ckey+k,'')!='':
               skip=True

            if not skip:
               v=q.get(k,'')

               format=tv.get('format','')
               if format!='' and v!='' and v!=None and v!="None":
                  v=format % float(v)

               if tv.get('json_and_pre','')=='yes' and v!='' and type(v)==dict:
                  v1=''
                  for kx in v:
                      v1+=kx+'='+str(v[kx])+'<br>'
                  v=v1

               if tv.get('starts_with','')=='yes':
                  v=''
                  for kx in sorted(q):
                      if kx!=k and kx.startswith(k):
                         v+=kx[len(k):-4]+'='+str(q.get(kx,''))+'<br>'

               v=str(v)

               cek=tv.get('check_extra_key','')
               if cek!='':
                  j=k.rfind('#')
                  if j>0:
                     k1=k[:j+1]+cek

                     v1=q.get(k1,'')

                     if format!='' and v1!='' and v1!=None:
                        v1=format % float(v1)

                     v1=str(v1)

                     if v1!='':
                        v+=' .. '+v1

               h+='   <td '+ha.replace('$#align#$',align)+'>'+v+'</td>\n'

        h+='  <tr>\n'

    h+='</table></small>\n'
    h+='</center>\n'

    if debug: h+='\n<p>Debug time (preparing html of a table): '+str(time.time()-dt)+' sec.<p>\n'

    if cmuoa=='':
        h+='</form>\n'

    # Add <br> to be able to select anchor on top
    for j in range(0,30):
        h+='<br>\n'

    return {'return':0, 'html':h, 'style':st}

##############################################################################
# show info for all layers

def html_viewer(i):
    """
    Input:  {
              data_uoa - CK entry UOA to view
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    duoa=i.get('data_uoa','')

    # Load entry
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    p=r['path']
    d=r['dict']

    dchars=d.get('characteristics',{})
    dchoices=d.get('choices',{})
    dmeta=d.get('meta',{})

    # Load stats
    dstat={}
    fstat=os.path.join(p,'ck-stat-flat-characteristics.json')
    if os.path.isfile(fstat):
        r=ck.load_json_file({'json_file':fstat, 'dict':dstat})
        if r['return']>0: return r
        dstat=r['dict']

    # Prepare table
    h=''
#    h+='<hr>\n'
    h+='<br>\n'
    h+='<center>\n'
    h+='<h2>DNN engine and model evaluation statistics per layer (crowd-tuning)</h2><br>\n'
    h+='</center>\n'

    xdeps=dmeta.get('xdeps',{})
    lcaffe=xdeps.get('lib-caffe',{})
    lmodel=xdeps.get('caffemodel',{})

    # Prepare extra info
    h+='<p>\n'
    h+='<table border="1" cellpadding="8" cellspacing="0">\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine name:</b></td>\n'
    h+='  <td>'+lcaffe.get('data_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine version:</b></td>\n'
    h+='  <td>'+lcaffe.get('ver','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine type:</b></td>\n'
    h+='  <td>'+dmeta.get('dnn_type','')+'</td>\n'
    h+=' </tr>\n'

    x=''

    dx=dmeta.get('xversions',{})
    for k in sorted(dx):
        v=dx[k]
        if v!='':
           if x!='': x+='<br>\n'
           x+=k+'='+str(v)+'\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN engine dependencies:</b></td>\n'
    h+='  <td>'+x+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN model name:</b></td>\n'
    h+='  <td>'+lmodel.get('data_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>DNN model version:</b></td>\n'
    h+='  <td>'+lmodel.get('ver','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>Batch size:</b></td>\n'
    h+='  <td>'+dchars.get('run',{}).get('REAL_ENV_CK_CAFFE_BATCH_SIZE','')+'</td>\n'
    h+=' </tr>\n'

# TBD: Need to show min,exp,max!
#    h+=' <tr>\n'
#    h+='  <td><b>FWBW time (ms.):</b></td>\n'
#    h+='  <td>'+str(dchars.get('run',{}).get('time_bw_ms',''))+'</td>\n'
#    h+=' </tr>\n'

#    h+=' <tr>\n'
#    h+='  <td><b>FW time (ms.):</b></td>\n'
#    h+='  <td>'+str(dchars.get('run',{}).get('time_fw_ms',''))+'</td>\n'
#    h+=' </tr>\n'

#    h+=' <tr>\n'
#    h+='  <td><b>BW time (ms.):</b></td>\n'
#    h+='  <td>'+str(dchars.get('run',{}).get('time_bw_ms',''))+'</td>\n'
#    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>Platform:</b></td>\n'
    h+='  <td>'+dmeta.get('plat_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>OS:</b></td>\n'
    h+='  <td>'+dmeta.get('os_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>CPU:</b></td>\n'
    h+='  <td>'+dmeta.get('cpu_name','')+'</td>\n'
    h+=' </tr>\n'

    h+=' <tr>\n'
    h+='  <td><b>GPU:</b></td>\n'
    h+='  <td>'+dmeta.get('gpu_name','')+'</td>\n'
    h+=' </tr>\n'


    h+=' </tr>\n'
    h+='</table>\n'

    h+='<center>\n'
    h+='<p>\n'
    h+='<table border="0" cellpadding="10" cellspacing="0">\n'

    h+=' <tr>\n'
    h+='  <td><b>Name</b></td>\n'
    h+='  <td><b>Direction</b></td>\n'
    h+='  <td align="right"><b>Min time (ms.):</b></td>\n'
    h+='  <td align="right"><b>Expected time (ms.):</b></td>\n'
    h+='  <td align="right"><b>Max time (ms.):</b></td>\n'
    h+='  <td align="right"><b>Repetitions:</b></td>\n'
    h+=' </tr>\n'

    # Detecting number of layers
    jj={}

    for j in range(0,1000):
        k3='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#min'
        v3=dstat.get(k3,'')

        if v3=='': break

        jj[j]=v3

    # Sorting by min time
    if i.get('all_params',{}).get('skip_sort','')!='yes':
       jj=sorted(jj, key=lambda x: jj[x], reverse=True)

    # Also layers
    for j in jj:
        k1='##characteristics#run#per_layer_info@'+str(j)+'#direction#min'
        k2='##characteristics#run#per_layer_info@'+str(j)+'#label#min'
        k3='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#min'
        k4='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#max'
        k5='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#exp_allx'
        k7='##characteristics#run#per_layer_info@'+str(j)+'#time_ms#repeats'

        v1=dstat.get(k1,'')
        v2=dstat.get(k2,'')
        v3=dstat.get(k3,'')
        v4=dstat.get(k4,'')
        v5=dstat.get(k5,[])
        v7=dstat.get(k7,'')

        if v1!='' and v2!='' and v3!='' and v4!='':
           v6=0
           if len(v5)>0:
              v6=v5[0]

           xv3=''
           xv4=''
           xv6=''

           if v3!='':
              if v3<0.1: xv3='0'
              else: xv3='<b>'+('%.1f'%v3)+'</b>'

           if v4!='':
              if v4<0.1: xv4='0'
              else: xv4='<b>'+('%.1f'%v4)+'</b>'

           if v6!='':
              if v6<0.1: xv6='0'
              else: xv6='<b>'+('%.1f'%v6)+'</b>'

           h+=' <tr>\n'
           h+='  <td>'+v2+'</td>\n'
           h+='  <td>'+v1+'</td>\n'
           h+='  <td align="right">'+xv3+'</td>\n'
           h+='  <td align="right">'+xv6+'</td>\n'
           h+='  <td align="right">'+xv4+'</td>\n'
           h+='  <td align="right">'+str(v7)+'</td>\n'
           h+=' </tr>\n'

    h+='</table>\n'

    h+='</center>\n'

    return {'return':0, 'html':h, 'show_top':'yes'}

##############################################################################
# replay experiment (TBD)

def replay(i):
    """
    Input:  {
              (data_uoa)
              (remote)

              (host_os)
              (target_os)
              (device_id)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    duoa=i.get('data_uoa','')
    remote=i.get('remote','')

    er=''
    esr=''

    if remote=='yes':
       er=i.get('exchange_repo','')
       if er=='': er=ck.cfg['default_exchange_repo_uoa']
       esr=i.get('exchange_subrepo','')
       if esr=='': esr=ck.cfg['default_exchange_subrepo_uoa']

    # Try to load info
    if o=='con':
       ck.out('Loading experiment entry ...')
       ck.out('')

    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa,
                 'repo_uoa':er,
                 'remote_repo_uoa':esr})
    if r['return']>0: return r

    d=r['dict']

    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # Check two main deps (engine and model)
    meta=d.get('meta',{})
    xdeps=meta.get('xdeps',{})

#    TBD: rebuild env by tags!
#
#    dnn=xdeps.get('lib-caffe',{})
#    model=xdeps.get('caffemodel',{})
#
#    pdnn=dnn.get('package_uoa','')
#    pmodel=model.get('package_uoa','')
#
#    preset_env={}
#    penv=[pdnn,pmodel]
#
#    for j in range(0, len(penv)):
#        px=''
#        py=penv[j]
#
#        if py!='':
#           # Search by package
#           r=ck.access({'action':'search',
#                        'module_uoa':cfg['module_deps']['env'],
#                        'search_dict':{'package_uoa':py}})
#           if r['return']>0: return r
#
#           l=r['lst']
#
#        if j==0: preset_env['lib-caffe']=px
#        elif j==1: preset_env['caffemodel']=px

    # Run pipeline
    choices=d.get('choices',{})
    
    # Clean various vars
    for k in replay_clean_vars:
        if k in choices:
           del(choices[k])

    if i.get('target_os','')!='' and not i['target_os'].startswith('android'):
       del(i['target_os'])

    env=choices.get('env',{})
    for k in replay_clean_env_vars:
        if k in env:
           del(env[k])
    choices['env']=env

    if hos!='': choices['host_os']=hos
    if tos!='': choices['target_os']=tos
    if tdid!='': choices['device_id']=tdid

    pipeline_data_uoa=choices['module_uoa']

    # Prepare pipeline
    ii={'action':'pipeline',
        'module_uoa':cfg['module_deps']['program'],
        'prepare':'yes',
        'choices':choices,
        'out':o}
    rr=ck.access(ii)
    if rr['return']>0: return rr

    fail=rr.get('fail','')
    if fail=='yes':
        return {'return':10, 'error':'pipeline failed ('+rr.get('fail_reason','')+')'}

    ready=rr.get('ready','')
    if ready!='yes':
        return {'return':11, 'error':'couldn\'t prepare universal CK program workflow'}

    # Run pipeline
    ii={'action':'run',
        'module_uoa':cfg['module_deps']['pipeline'],
        'data_uoa':pipeline_data_uoa,
        'pipeline':rr,
        'out':o}
    rr=ck.access(ii)
    if rr['return']>0: return rr

    fail=rr.get('fail','')
    if fail=='yes':
        return {'return':10, 'error':'pipeline failed ('+rr.get('fail_reason','')+')'}

    if o=='con':
       ck.out('')
       ck.out('Your results:')
       ck.out('')

       dstat=rr.get('last_stat_analysis',{}).get('dict_flat',{})

       x0=dstat.get("##characteristics#run#time_fwbw_ms#min",None)
       x0e=dstat.get("##characteristics#run#time_fwbw_ms#exp",None)

       if x0!=None:
            ck.out('* FWBW min: '+('%.0f'%x0)+' ms.')
       if x0e!=None:
            ck.out('* FWBW exp: '+('%.0f'%x0e)+' ms.')

       x1=dstat.get("##characteristics#run#time_fw_ms#min",None)
       x1e=dstat.get("##characteristics#run#time_fw_ms#exp",None)

       if x1!=None:
            ck.out('* FW   min: '+('%.0f'%x1)+' ms.')
       if x1e!=None:
            ck.out('* FW   exp: '+('%.0f'%x1e)+' ms.')

       x2=dstat.get("##characteristics#run#time_bw_ms#min",None)
       x2e=dstat.get("##characteristics#run#time_bw_ms#exp",None)

       if x2!=None:
            ck.out('* BW   min: '+('%.0f'%x2)+' ms.')
       if x2e!=None:
            ck.out('* BW   exp: '+('%.0f'%x2e)+' ms.')

    return {'return':0}

##############################################################################
# see ReQuEST results (CK Dashboard)

def dashboard(i):
    """
    Input:  {
              (host)        - Internal web server host
              (port)        - Internal web server port

              (wfe_host)    - External web server host
              (wfe_port)    - External web server port

              (extra_url)   - extra URL

              (results)     - repo with experiments to visualize (will be added as &results=... to extra_url)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

#    Old style
#    i['action']='browser'
#    i['cid']=''
#    i['module_uoa']=''
#    i['template']='nntest'


    i['action']='start'
    i['module_uoa']='web'
    i['browser']='yes'
    i['template']='request.asplos18'
    i['cid']=''

    if i.get('results','')!='':
       x=i.get('extra_url','')
       x+='&results='+i['results']
       i['extra_url']=x

    return ck.access(i)

##############################################################################
# prepare common meta for ReQuEST @ ASPLOS"18

def prepare_common_meta(i):
    """
    Input:  {
              platform_dict - output from platform detection
              request_dict  - info about ReQuEST submission
              deps          - resolved deps to summarize deps (package, tags, version)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              tags        - tags for experiment entry
              meta        - meta for experiment entry
              record_dict - dict to update records
            }

    """

    from time import strftime, gmtime
    import copy

    # Get current timestamp
    r=ck.get_current_date_time({})
    if r['return']>0: return r
    timestamp=r['iso_datetime']

    #striped timestamp
    j=timestamp.find('.')
    if j>0: timestamp=timestamp[:j]

    stimestamp=timestamp.replace('-','').replace(':','').replace('T','')

    pi=i['platform_dict']
    rd=i['request_dict']
    deps=i.get('deps',{})

    # Prepare tags
    tags=[
      'request',
      'request-asplos18',
      timestamp,
      stimestamp
    ]

    tags.append(rd['algorithm_species'])

    # Prepare meta
    meta=copy.deepcopy(rd)

    meta['timestamp']=timestamp
    meta['stimestamp']=stimestamp

    meta['request_version']=1

    # Check platform
    hos=pi['host_os_uoa']
    hos_uid=pi['host_os_uid']
    hosd=pi['host_os_dict']

    tos=pi['os_uoa']
    tos_uid=pi['os_uid']
    tosd=pi['os_dict']
    tbits=tosd.get('bits','')

    remote=tosd.get('remote','')

    tdid=pi['device_id']

    features=pi.get('features',{})

    fplat=features.get('platform',{})
    fos=features.get('os',{})
    fcpu=features.get('cpu',{})

    plat_name=fplat.get('name','')
    plat_uid=features.get('platform_uid','')
    os_name=fos.get('name','')
    os_uid=features.get('os_uid','')
    cpu_name=fcpu.get('name','')
    cpu_abi=fcpu.get('cpu_abi','')
    if cpu_name=='' and cpu_abi!='': cpu_name='unknown-'+cpu_abi
    cpu_uid=features.get('cpu_uid','')
    sn=fos.get('serial_number','')

    # Check if CPU clusters (TBD: need to know which one is actually used!)
    if cpu_name=='':
       ufcpu=features.get('cpu_unique',[])
       if len(ufcpu)>1:
           for q in ufcpu:
               if cpu_name!='': cpu_name+=' ; '
               x=q.get('ck_cpu_name','')
               if x!='': cpu_name+=x

    # GPU
    fgpu=features.get('gpu',{})
    gpu_name=fgpu.get('name','')

    gpgpu0=features.get('gpgpu',{})
    if type(gpgpu0)==list:
       if len(gpgpu0)>0:
          gpgpu0=gpgpu0[0]
    fgpgpu=gpgpu0.get('gpgpu',{})

    gpgpu_name=fgpgpu.get('name','')
    gpgpu_vendor=fgpgpu.get('vendor','')
    gpgpu_type=fgpgpu.get('type','')

    gpgpu_name2=gpgpu_name
    if gpgpu_vendor!='': gpgpu_name2=gpgpu_vendor+' '+gpgpu_name

    fgpgpu_misc=gpgpu0.get('gpgpu_misc',{})
    opencl=fgpgpu_misc.get('opencl c version','')

    # Assembling meta for platform
    meta.update({
                 'scenario_module_uoa': work['self_module_uid'],

                 'host_os_uid':hos_uid,
                 'target_os_uid':tos_uid,
                 'target_device_id':tdid,

                 'cpu_name':cpu_name,
                 'cpu_abi':cpu_abi,
                 'cpu_uid':cpu_uid,

                 'os_name':os_name,
                 'os_uid':os_uid,

                 'plat_name':plat_name,
                 'plat_uid':plat_uid,

                 'gpu_name':gpu_name,
                 'gpgpu_name':gpgpu_name2,
                 'gpgpu_vendor':gpgpu_vendor,
                 'opencl':opencl
                })

    # Process dependencies
    r=ck.access({'action':'deps_summary',
                 'module_uoa':cfg['module_deps']['env'],
                 'deps':deps})
    if r['return']>0: return r
    deps_summary=r['deps_summary']

    meta['deps_summary']=deps_summary

    # Misc info
    rd={
         'subview_uoa':'f84ca49f79a1446a'  # ReQuEST default table view from ck-autotuning repo
                                           # ck-autotuning:experiment.view:request-default
       }

    return {'return':0, 'tags':tags, 'meta':meta, 'record_dict':rd}

##############################################################################
# move validated experiment to an official repo

def validate(i):
    """
    Input:  {
              (experiment) - experiment UOA
              (point)      - point to move
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import shutil

    experiment=i.get('experiment','')

    if experiment=='':
       return {'return':1, 'error':'experiment is not defined'}

    # Find experiment
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'data_uoa':experiment})
    if r['return']>0: return r

    duid=r['data_uid']
    duoa=r['data_uoa']

    d=r['dict']
    p=r['path']

    # Check if entry is already there 
    r=ck.access({'action':'update',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'repo_uoa':repo_with_validated_results,
                 'data_uoa':'validated-'+duoa,
                 'dict':d,
                 'common_func':'yes',
                 'substitute':'yes',
                 'sort_keys':'yes'})
    if r['return']>0: return r             

    nduid=r['data_uid']
    np=r['path']

    # Check point
    point=i.get('point','')

    if point!='':
       p1=os.listdir(p)
       for d in p1:
           if d.startswith('ckp-'+point+'.'):
              pf1=os.path.join(p,d)
              pf2=os.path.join(np,d)

              shutil.copyfile(pf1,pf2)

    ck.out('Copied to '+np)

    return {'return':0}

##############################################################################
# make full name for dependency

def make_deps_full_name(i):
    """
    Input:  {
              deps - dict with deps
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              full_name    - full name of deps
            }

    """

    x=i['deps']

    y=str(x.get('data_name',''))

    y1=str(x.get('version',''))
    if y1!='': y+=' '+y1

    y1=str(x.get('git_revision',''))
    if y1!='': y+=' ('+y1+')'

    return {'return':0, 'full_name':y}

##############################################################################
# check label in value

def check_label(v, ldim):

    if type(v)!=float and type(v)!=int: 
       v=str(v)

       label=0
       found=False
       for k in ldim:
           if k==v:
              v=ldim[k]
              found=True
              break
           else:
              if ldim[k]>label: 
                 label=ldim[k]

       if not found:
          ldim[v]=label+1
          v=label+1

    return v

##############################################################################
# check label in value

def html_labels(i):

    ldim=i['labels']
    axis=i['axis']

    muoa=i.get('module_uoa','')

    h=''
    h1='<small><b>Labels '+axis+': </b>\n'
    for j in range(1,10000):
        l=None
        for k in ldim:
            v=ldim[k]
            if v==j:
               l=k
               break

        if l==None:
           break

        if muoa!='':
           r=ck.access({'action':'load', 'module_uoa':muoa, 'data_uoa':l})
           if r['return']==0:
              l=r['data_name']

        if l!='' and l!=None:
           h+=str(j)+') '+l+'; '

    if h!='':
       h=h1+h+'<br>\n'

    return {'return':0, 'html':h}

##############################################################################
# start scoreboard

def scoreboard(i):
    return dashboard(i)
